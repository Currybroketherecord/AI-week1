import re

class myCryptochatbot:
    def __init__(self):
        self.name = "CryptoBuddy"
        self.description = "A professional yet friendly chatbot that analyzes cryptocurrency trends, sustainability, and profitability."
        self.version = "1.2"
        self.crypto_db = {  
            "Bitcoin": {  
                "price_trend": "rising",  
                "market_cap": "high",  
                "energy_use": "high",  
                "sustainability_score": 3/10  
            },  
            "Ethereum": {  
                "price_trend": "stable",  
                "market_cap": "high",  
                "energy_use": "medium",  
                "sustainability_score": 6/10  
            },  
            "Cardano": {  
                "price_trend": "rising",  
                "market_cap": "medium",  
                "energy_use": "low",  
                "sustainability_score": 8/10  
            }  
        }
        
        self.synonyms = {
            "trending": ["trending", "popular", "high demand", "moving up", "trends"],
            "sustainable": ["sustainable", "eco-friendly", "green", "low energy"],
            "profitable": ["profit", "profitable", "returns", "gain"]
        }

    def identify_category(self, user_query):
        """Identify the category based on recognized synonyms."""
        for category, keywords in self.synonyms.items():
            if any(word in user_query for word in keywords):
                return category
        return None

    def sort_cryptos(self, category, order="descending"):
        """Sort cryptocurrencies based on category and order preference."""
        key = {
            "sustainable": lambda coin: self.crypto_db[coin]["sustainability_score"],
            "profitable": lambda coin: {"low": 1, "medium": 2, "high": 3}[self.crypto_db[coin]["market_cap"]],
            "trending": lambda coin: {"stable": 1, "rising": 2}[self.crypto_db[coin]["price_trend"]]
        }.get(category)

        sorted_cryptos = sorted(self.crypto_db.keys(), key=key, reverse=(order == "descending"))
        return sorted_cryptos

    def respond(self, user_query):
        user_query = user_query.lower()
        category = self.identify_category(user_query)
        if not category:
            return "I appreciate your curiosity! Try asking about trends, sustainability, or profitability, and I'll guide you through crypto insights."

        # Detect sorting order properly
        if "least" in user_query:
            order = "ascending"
        elif "most" in user_query:
            order = "descending"
        else:
            order = "ascending" if category == "sustainable" else "descending"  # Logical default

        sorted_coins = self.sort_cryptos(category, order)
        return f"{'Most' if order == 'descending' else 'Least'} {category} coin(s): {', '.join(sorted_coins)}. Hope that helps! 🚀"

# Instantiate chatbot correctly with a friendly welcome message
if __name__ == "__main__":
    print("👋 Welcome to CryptoBuddy! I'm here to help you navigate crypto investments professionally and easily.")
    bot = myCryptochatbot()
    while True:
        user_query = input("\nYou: ")
        if user_query.lower() in ["exit", "quit"]:
            print("🚀 Thanks for chatting! Stay smart with your crypto investments, and feel free to return anytime.")
            break
        response = bot.respond(user_query)
        print(f"{bot.name}: {response}")