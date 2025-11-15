import React, { useState } from "react";
import { ShoppingBag, Utensils, User, AlertCircle, Clock, Tag } from "lucide-react";

// ---------------- Types ----------------

type PreferenceType = "dietary" | "allergens" | "categories";

interface FoodItem {
  id: number;
  name: string;
  restaurant: string;
  category: string;
  originalPrice: number;
  discountedPrice: number;
  quantity: number;
  pickupWindow: string;
  expiryDate: string;
  allergens: string[];
  dietaryTags: string[];
  image: string;
  type: "surprise" | "custom";
}

interface PreferencesState {
  dietary: string[];
  allergens: string[];
  categories: string[];
}

// ---------------- Mock Data ----------------

const mockFoodItems: FoodItem[] = [
  {
    id: 1,
    name: "Fresh Bakery Bundle",
    restaurant: "Corner Bakery",
    category: "Bakery",
    originalPrice: 15.99,
    discountedPrice: 4.99,
    quantity: 3,
    pickupWindow: "6:00 PM - 7:00 PM",
    expiryDate: "Today",
    allergens: ["gluten", "dairy", "eggs"],
    dietaryTags: ["vegetarian"],
    image: "🥖",
    type: "surprise",
  },
  {
    id: 2,
    name: "Mediterranean Salad Box",
    restaurant: "Fresh Greens Cafe",
    category: "Salads",
    originalPrice: 12.99,
    discountedPrice: 5.99,
    quantity: 2,
    pickupWindow: "7:00 PM - 8:00 PM",
    expiryDate: "Today",
    allergens: ["dairy"],
    dietaryTags: ["vegetarian", "gluten-free"],
    image: "🥗",
    type: "custom",
  },
  {
    id: 3,
    name: "Pizza Slice Pack",
    restaurant: "Tony's Pizzeria",
    category: "Italian",
    originalPrice: 18.0,
    discountedPrice: 0,
    quantity: 1,
    pickupWindow: "8:00 PM - 9:00 PM",
    expiryDate: "Today",
    allergens: ["gluten", "dairy"],
    dietaryTags: ["vegetarian"],
    image: "🍕",
    type: "surprise",
  },
  {
    id: 4,
    name: "Sushi Assortment",
    restaurant: "Sakura Sushi",
    category: "Japanese",
    originalPrice: 22.0,
    discountedPrice: 8.99,
    quantity: 2,
    pickupWindow: "6:30 PM - 7:30 PM",
    expiryDate: "Today",
    allergens: ["fish", "soy"],
    dietaryTags: ["pescatarian", "dairy-free"],
    image: "🍣",
    type: "custom",
  },
];

const userPreferences = {
  dietaryRestrictions: ["vegetarian", "gluten-free", "vegan", "pescatarian"],
  allergens: ["gluten", "dairy", "eggs", "nuts", "soy", "fish", "shellfish"],
  categories: ["Bakery", "Salads", "Italian", "Japanese", "Mexican", "American"],
};

// ---------------- Component ----------------

function FoodRescueApp() {
  const [activeTab, setActiveTab] = useState<"browse" | "custom" | "preferences">("browse");

  const [preferences, setPreferences] = useState<PreferencesState>({
    dietary: [],
    allergens: [],
    categories: [],
  });

  const tabs = [
    { id: "browse", label: "Surprise Bags", icon: ShoppingBag },
    { id: "custom", label: "Custom Selection", icon: Utensils },
    { id: "preferences", label: "Preferences", icon: User },
  ];

  const filteredItems = mockFoodItems.filter((item) => {
    if (activeTab === "browse") return item.type === "surprise";
    if (activeTab === "custom") return item.type === "custom";
    return true;
  });

  // --------- FIXED: Fully type-safe toggle ---------
  const handlePreferenceToggle = (type: PreferenceType, value: string) => {
    setPreferences((prev) => ({
      ...prev,
      [type]: prev[type].includes(value)
        ? prev[type].filter((item) => item !== value)
        : [...prev[type], value],
    }));
  };

  // ---------------- JSX ----------------

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      <div className="max-w-6xl mx-auto p-6">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-green-700 mb-2">🌱 Food Rescue</h1>
          <p className="text-gray-600">Save food, save money, save the planet</p>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 bg-white rounded-lg p-2 shadow-md">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-md transition-all ${
                  activeTab === tab.id
                    ? "bg-green-600 text-white shadow-md"
                    : "bg-white text-gray-600 hover:bg-gray-50"
                }`}
              >
                <Icon size={20} />
                <span className="font-medium">{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Browse / Custom */}
        {(activeTab === "browse" || activeTab === "custom") && (
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-gray-800">
                {activeTab === "browse" ? "🎁 Free Surprise Bags" : "🍽️ Custom Selection"}
              </h2>
              <span className="text-sm text-gray-600">
                {activeTab === "browse" ? "Free!" : "Discounted prices"}
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredItems.map((item) => (
                <div
                  key={item.id}
                  className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow overflow-hidden"
                >
                  <div className="bg-gradient-to-br from-green-400 to-blue-400 p-6 text-center">
                    <div className="text-6xl mb-2">{item.image}</div>
                    <h3 className="text-xl font-bold text-white">{item.name}</h3>
                    <p className="text-white text-sm opacity-90">{item.restaurant}</p>
                  </div>

                  <div className="p-4">
                    {/* Pricing */}
                    <div className="flex items-center justify-between mb-3">
                      {item.discountedPrice === 0 ? (
                        <span className="text-2xl font-bold text-green-600">FREE</span>
                      ) : (
                        <div className="flex items-center gap-2">
                          <span className="text-2xl font-bold text-green-600">
                            ${item.discountedPrice}
                          </span>
                          <span className="text-sm text-gray-400 line-through">
                            ${item.originalPrice}
                          </span>
                        </div>
                      )}
                      <span className="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs font-medium">
                        {item.quantity} left
                      </span>
                    </div>

                    {/* Info */}
                    <div className="space-y-2 mb-4">
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <Clock size={16} />
                        <span>{item.pickupWindow}</span>
                      </div>
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <Tag size={16} />
                        <span>{item.category}</span>
                      </div>
                    </div>

                    {/* Dietary + Allergens */}
                    <div className="mb-3">
                      <div className="flex flex-wrap gap-1 mb-2">
                        {item.dietaryTags.map((tag) => (
                          <span
                            key={tag}
                            className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>

                      {item.allergens.length > 0 && (
                        <div className="flex items-start gap-1">
                          <AlertCircle size={14} className="text-orange-500 mt-1 flex-shrink-0" />
                          <span className="text-xs text-gray-500">
                            Contains: {item.allergens.join(", ")}
                          </span>
                        </div>
                      )}
                    </div>

                    <button className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg font-medium transition-colors">
                      {activeTab === "browse" ? "Reserve Free Bag" : "Add to Cart"}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Preferences */}
        {activeTab === "preferences" && (
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Set Your Preferences</h2>

            <div className="space-y-6">
              {/* Dietary */}
              <div>
                <h3 className="text-lg font-semibold text-gray-700 mb-3">Dietary Preferences</h3>
                <div className="flex flex-wrap gap-2">
                  {userPreferences.dietaryRestrictions.map((diet) => (
                    <button
                      key={diet}
                      onClick={() => handlePreferenceToggle("dietary", diet)}
                      className={`px-4 py-2 rounded-full font-medium transition-all ${
                        preferences.dietary.includes(diet)
                          ? "bg-green-600 text-white shadow-md"
                          : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                      }`}
                    >
                      {diet}
                    </button>
                  ))}
                </div>
              </div>

              {/* Allergens */}
              <div>
                <h3 className="text-lg font-semibold text-gray-700 mb-3">Allergen Alerts</h3>
                <div className="flex flex-wrap gap-2">
                  {userPreferences.allergens.map((allergen) => (
                    <button
                      key={allergen}
                      onClick={() => handlePreferenceToggle("allergens", allergen)}
                      className={`px-4 py-2 rounded-full font-medium transition-all ${
                        preferences.allergens.includes(allergen)
                          ? "bg-red-600 text-white shadow-md"
                          : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                      }`}
                    >
                      {allergen}
                    </button>
                  ))}
                </div>
              </div>

              {/* Categories */}
              <div>
                <h3 className="text-lg font-semibold text-gray-700 mb-3">Favorite Categories</h3>
                <div className="flex flex-wrap gap-2">
                  {userPreferences.categories.map((category) => (
                    <button
                      key={category}
                      onClick={() => handlePreferenceToggle("categories", category)}
                      className={`px-4 py-2 rounded-full font-medium transition-all ${
                        preferences.categories.includes(category)
                          ? "bg-blue-600 text-white shadow-md"
                          : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                      }`}
                    >
                      {category}
                    </button>
                  ))}
                </div>
              </div>

              <button className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-medium text-lg transition-colors mt-6">
                Save Preferences
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default FoodRescueApp;
