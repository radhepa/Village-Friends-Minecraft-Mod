package dev.villagefriends;

import java.util.UUID;

/** Handwritten dialogue: no online account, API key, or subscription is needed. */
public final class Dialogue {
    private static final String[] PERSONALITIES = {"Warmhearted", "Adventurous", "Thoughtful", "Playful"};

    public static String name(UUID uuid) {
        return name(uuid,ResidentAppearance.generate(uuid));
    }
    public static String name(UUID uuid,String look) {return ResidentNames.name(uuid,look);}
    public static String personality(UUID uuid) { return PERSONALITIES[Math.floorMod(uuid.hashCode(), 4)]; }

    public static String greeting(String name, int level, boolean baby, long day) {
        if (baby) return "Hello! Will you tell me about your adventures? One day I'll explore the world too!";
        return switch (level) {
            case 4 -> "My best friend! The village feels like home whenever you're here. Sit and stay a while.";
            case 3 -> "There you are! I was hoping you'd visit. It's always good to spend time with you.";
            case 2 -> "Hello, friend! How have your adventures been? I've saved a little time for a chat.";
            case 1 -> "It's good to see you again! I'm starting to look forward to your visits.";
            default -> "Hello, traveler! I'm " + name + ". It's nice to meet someone new. How's your day going?";
        };
    }

    public static String conversation(UUID uuid, String topic, String profession, boolean baby, long day, int level) {
        int variant = Math.floorMod(uuid.hashCode() + day, 4);
        if (baby) return switch (topic) {
            case "adventure" -> "You went exploring? Did you see a dragon? Or a really, really big chicken?";
            case "work" -> "I'm practicing my grown-up 'hrrmm.' Do you think I sound convincing?";
            case "joke" -> "Why did the chicken cross the village? To get to the other seed! Hee hee!";
            default -> "I found a beetle near the bell! I'm calling it Captain Tiny. Want to be friends too?";
        };
        return switch (topic) {
            case "work" -> work(profession, variant);
            case "adventure" -> switch (variant) {
                case 0 -> "I've heard there are mountains taller than the clouds. If you go, bring back a story!";
                case 1 -> "A traveler told me about glowing caves. Imagine a whole ceiling full of little stars.";
                case 2 -> "I like exploring, but the iron golem says wandering after sunset is a terrible idea.";
                default -> level >= 2 ? "Promise you'll come back safe? Adventures sound grand, but I'd miss my friend."
                        : "The world is so big. Sometimes I wonder what lies beyond the next river.";
            };
            case "joke" -> switch (variant) {
                case 0 -> "Why don't skeletons enjoy parties? They have no body to dance with! Hrr-hrr!";
                case 1 -> "I asked a creeper for gardening advice. It said my flowerbed needed more 'boom.'";
                case 2 -> "My neighbor calls me a square. In this village, I think that's a compliment.";
                default -> "What's an iron golem's favorite flower? A poppy, of course. It has excellent taste.";
            };
            default -> switch (variant) {
                case 0 -> "A quiet morning, warm bread, and a friendly face. That's my idea of a perfect day.";
                case 1 -> "The bell sounded lovely today. Somehow our little village always finds its rhythm.";
                case 2 -> "I planted flowers near my door. A little color makes even a rainy day feel brighter.";
                default -> level >= 2 ? "I've been smiling more since we became friends. Thanks for making time for me."
                        : "It's nice when someone stops to say hello instead of rushing straight to the trading stall.";
            };
        };
    }

    private static String work(String profession, int variant) {
        return switch (profession) {
            case "farmer" -> "The crops are coming along nicely. There's something wonderful about helping a tiny seed grow.";
            case "librarian" -> "Every book is a little doorway. Today I found one about a very stubborn wandering trader.";
            case "fisherman" -> "The river was peaceful today. I caught a fish so big... well, it got away before anyone saw it.";
            case "fletcher" -> "A good arrow needs balance and patience. Like a friendship, I suppose!";
            case "cleric" -> "I've been studying amethyst. Even the smallest shard has a little wonder in it.";
            case "cartographer" -> "My newest map has an empty corner. That's my favorite part: there's still something to discover.";
            case "armorer" -> "An honest day's work at the forge keeps our neighbors safe. That makes the heat worth it.";
            case "toolsmith" -> "A well-made tool can last for years. Care for it, and it'll always be there when you need it.";
            case "weaponsmith" -> "I hope my swords spend more time on the wall than in a battle. Peace suits this village.";
            case "leatherworker" -> "I finished a new pair of boots. Comfortable shoes make every journey a little better.";
            case "mason" -> "I love finding patterns in stone. Even a plain block can become something beautiful.";
            case "shepherd" -> "The sheep have been very chatty. I think they're reviewing my choice of wool colors.";
            case "butcher" -> "Sharing a good meal brings neighbors together. You're welcome at my table anytime.";
            case "knight" -> "A reliable shield and a little practice go a long way. Our neighbors deserve to feel safe.";
            case "archer" -> "Steady hands, a straight arrow, and patience. That's the secret to a good shot.";
            case "cook" -> "Warm bread and a hearty stew make a fine welcome. There's always room for one more at the table.";
            case "tavern_keeper" -> "The best part of a tavern is the company. Stop by for a mug and a friendly conversation.";
            case "apothecary" -> "I keep bandages and smelling salts ready. A little preparation can make a great difference.";
            case "painter" -> "This village has so many colors. I'm trying to capture a little of its warmth on canvas.";
            case "bard" -> "A melody can bring a whole room together. I'm working on a tune for our village.";
            case "tailor" -> "Good clothes should feel like they belong to you. I'm especially fond of a well-made rain cloak.";
            case "carpenter" -> "A sturdy bench gives neighbors a place to gather. Small things can make a village feel like home.";
            case "scholar" -> "Every neighbor has a story worth keeping. Our archives help us remember where we came from.";
            case "nitwit" -> "Work? Today I'm testing how comfortable the grass is. Very important research.";
            default -> "I'm still finding my place here. Until then, there's always a neighbor who could use a hand.";
        };
    }

    private Dialogue() {}
}
