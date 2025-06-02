import re

class myCryptochatbot:
    def __init__(self):
        self.name = "CryptoBuddy"
        self.description = "A rule-based chatbot that analyzes cryptocurrency data and provides investment advice based on profitability and sustainability"
        self.version = "1.1"
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
            return "Sorry, I didn't understand your question. Try asking about trends, sustainability, or profitability."
       
        if "least" in user_query:
            order = "ascending"
        elif "most" in user_query:
            order = "descending"
        else:
            order = "ascending" if category == "sustainable" else "descending"
        # --- Advice Rules ---
        filtered = []
        if category == "profitable":
            if order == "descending":
                # Most profitable
                filtered = [
                    coin for coin, data in self.crypto_db.items()
                    if data["price_trend"] == "rising" and data["market_cap"] == "high"
                ]
            else:
                # Least profitable
                filtered = [
                    coin for coin, data in self.crypto_db.items()
                    if data["price_trend"] != "rising" or data["market_cap"] != "high"
                ]
        elif category == "sustainable":
            if order == "descending":
                # Most sustainable
                filtered = [
                    coin for coin, data in self.crypto_db.items()
                    if data["energy_use"] == "low" and data["sustainability_score"] > 0.7
                ]
            else:
                # Least sustainable
                filtered = [
                    coin for coin, data in self.crypto_db.items()
                    if data["energy_use"] != "low" or data["sustainability_score"] <= 0.7
                ]

        # If advice rule found coins, sort and return them according to order
        sorted_filtered = []
        if filtered:
            sorted_filtered = self.sort_cryptos(category, order)
            # Only show coins that are in the filtered list
            sorted_filtered = [coin for coin in sorted_filtered if coin in filtered]
        if sorted_filtered:
            return f"{'Most' if order == 'descending' else 'Least'} {category} coin(s): {', '.join(sorted_filtered)}."

        # If no advice rule match, sort all coins in the category
        sorted_coins = self.sort_cryptos(category, order)
        return f"{'Most' if order == 'descending' else 'Least'} {category} coin(s): {', '.join(sorted_coins)}."

# Instantiate chatbot correctly
if __name__ == "__main__":
    bot = myCryptochatbot()
    while True:
        user_query = input("You: ")
        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = bot.respond(user_query)  
        print(f"{bot.name}: {response}")