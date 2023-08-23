{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "source": [
        "## Import Libraries"
      ],
      "metadata": {
        "id": "j6W1qNn6_90i"
      }
    },
    {
      "cell_type": "code",
      "execution_count": 12,
      "metadata": {
        "id": "9dTiLjhXVd4C",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "3897b35e-b472-4795-8f40-3d1ee08f77d4"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "[nltk_data] Downloading package stopwords to /root/nltk_data...\n",
            "[nltk_data]   Package stopwords is already up-to-date!\n"
          ]
        }
      ],
      "source": [
        "import pandas as pd\n",
        "import gensim\n",
        "from gensim import corpora\n",
        "from gensim.models import LdaModel\n",
        "from gensim.models.coherencemodel import CoherenceModel\n",
        "import nltk\n",
        "from nltk.corpus import stopwords\n",
        "nltk.download('stopwords')\n",
        "import matplotlib.pyplot as plt"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "## Define the main function"
      ],
      "metadata": {
        "id": "dR1VajTXAEzR"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "def main(num_topics_range):\n",
        "    # Read the CSV file\n",
        "    npr = pd.read_csv('./Files/npr.csv')\n",
        "\n",
        "    # Extract the text column\n",
        "    text_column = npr['Article']  # Replace 'text_column_name' with the actual column name\n",
        "\n",
        "    # Preprocess the text\n",
        "    def preprocess_text(text):\n",
        "        stop_words = set(stopwords.words('english'))\n",
        "        tokens = [word for word in text.lower().split() if word not in stop_words]\n",
        "        return tokens\n",
        "\n",
        "    tokenized_documents = [preprocess_text(text) for text in text_column]\n",
        "\n",
        "    # Create a dictionary representation of the documents\n",
        "    dictionary = corpora.Dictionary(tokenized_documents)\n",
        "\n",
        "    # Convert the tokenized documents into a bag-of-words corpus\n",
        "    corpus = [dictionary.doc2bow(doc) for doc in tokenized_documents]\n",
        "\n",
        "    coherence_scores = []\n",
        "\n",
        "    for num_topics in num_topics_range:\n",
        "        lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary)\n",
        "        coherence_model = CoherenceModel(model=lda_model, texts=tokenized_documents, dictionary=dictionary, coherence='c_v')\n",
        "        coherence_score = coherence_model.get_coherence()\n",
        "        coherence_scores.append((num_topics, coherence_score))\n",
        "\n",
        "        print(f\"Number of Topics: {num_topics}, Coherence Score: {coherence_score:.4f}\")\n",
        "\n",
        "    # Plot coherence scores\n",
        "    num_topics, scores = zip(*coherence_scores)\n",
        "    plt.plot(num_topics, scores)\n",
        "    plt.xlabel(\"Number of Topics\")\n",
        "    plt.ylabel(\"Coherence Score\")\n",
        "    plt.title(\"Coherence Score for Different Numbers of Topics\")\n",
        "    plt.show()"
      ],
      "metadata": {
        "id": "Q6qvNwSk9gZ6"
      },
      "execution_count": 15,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "## Function Execution"
      ],
      "metadata": {
        "id": "I-oaH8QPAJxj"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "if __name__ == '__main__':\n",
        "    num_topics_range = range(2, 10)\n",
        "    main(num_topics_range)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "9Ta9gVpd_6qq",
        "outputId": "bc7cc79a-6d63-4303-886d-c5bfa71b39ad"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "WARNING:gensim.models.ldamodel:too few updates, training might not converge; consider increasing the number of passes or iterations to improve accuracy\n",
            "WARNING:gensim.models.ldamodel:too few updates, training might not converge; consider increasing the number of passes or iterations to improve accuracy\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Number of Topics: 2, Coherence Score: 0.2304\n"
          ]
        }
      ]
    }
  ]
}
