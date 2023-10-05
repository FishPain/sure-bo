import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

df = pd.read_csv("src/datasets/emscad_v1.csv", encoding="ISO-8859-1")

category_mapping = {
    "Business": ["business", "sales", "marketing", "accounting", "finance"],
    "Human Resource": ["admin", "adminstrative"],
    "Mass Communications": [
        "advertising",
        "entertainment",
        "public relations",
        "arts",
        "creative design",
    ],
    "Hotel": ["tourism", "hotel"],
    "Educator": ["teach", "training", "lecture"],
    "Manufacturing": [
        "process control",
        "quality assurance",
        "maintenance",
        "manufacturing",
        "purchasing",
    ],
    "Construction": [
        "real estate",
        "housing",
        "constructions",
        "architect",
        "interior design",
    ],
    "Healthcare": ["pharmacy", "practitioner", "diagnosis"],
    "Science": [
        "agriculture",
        "food technology",
        "biology",
        "chemistry",
        "physics",
        "biomedical",
        "science",
        "biotechnology",
        "geology",
    ],
    "engineering": ["engineer", "mechanical", "electrical", "civil"],
    "IT": ["IT", "information technology", "developer", "programmer"],
}


def categorise_job_title(title, category_mapping=category_mapping):
    for category, keywords in category_mapping.items():
        for keyword in keywords:
            if str(keyword).lower() in str(title).lower():
                return category
    return "Other"


# Apply the categorization function to the job titles and create a new 'Category' column
df["Category"] = df["title"].apply(lambda x: categorise_job_title(x, category_mapping))

df["IsOther"] = df["Category"] == "Other"
category_counts = df["Category"].value_counts()

df["Category"].value_counts()

fraud_counts = df.groupby(["Category", "fraudulent"]).size().unstack().fillna(0)

ax = fraud_counts.plot(kind="barh", stacked=True)
plt.xlabel("Count")
plt.ylabel("Job Category")
plt.title("Number of Fraudulent vs. Non-Fraudulent Entries by Job Category")

for p in ax.patches:
    width = p.get_width()
    height = p.get_height()
    x, y = p.get_xy()
    ax.annotate(f"{int(height)}", (x + width / 2, y + height), ha="center")

plt.legend(title="Fraudulent", labels=["Not Fraudulent", "Fraudulent"])

for i, count in enumerate(category_counts):
    plt.text(count, i, str(count), ha="left", va="center")
plt.show()

keywords_fraudulent = [
    "work from home",
    "wfh",
]


def using_keywords(text, keywords):
    words = text.lower().split()
    selected_words = [word for word in words if word in keywords]
    return " ".join(selected_words)


non_fraudulent_text = " ".join(df[df["fraudulent"] == "f"]["description"].astype(str))
fraudulent_text = " ".join(df[df["fraudulent"] == "t"]["description"].astype(str))

wordcloud_non_fraudulent = WordCloud(
    width=800, height=400, background_color="white"
).generate(non_fraudulent_text)
wordcloud_fraudulent = WordCloud(
    width=800, height=400, background_color="white"
).generate(fraudulent_text)

plt.figure(figsize=(15, 6))

plt.subplot(1, 2, 1)
plt.imshow(wordcloud_non_fraudulent, interpolation="bilinear")
plt.title("Non-Fraudulent Job Descriptions")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(wordcloud_fraudulent, interpolation="bilinear")
plt.title("Fraudulent Job Descriptions")
plt.axis("off")

plt.tight_layout()
plt.show()
