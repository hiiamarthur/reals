class DateType {
  static const String outdoor = 'outdoor';
  static const String indoor = 'indoor';
  static const String adventure = 'adventure';
  static const String cultural = 'cultural';
  static const String relaxation = 'relaxation';
  static const String exhibition = 'exhibition';
  static const String music = 'music';
  static const String creative = 'creative';
  static const String entertainment = 'entertainment';
  static const String sport = 'sport';
  static const String nightlife = 'nightlife';
  static const String nature = 'nature';
  static const String shopping = 'shopping';

  // Add a list of all types for easier iteration if needed
  static const List<String> allTypes = [
    outdoor,
    indoor,
    adventure,
    cultural,
    relaxation,
    exhibition,
    music,
    creative,
    entertainment,
    sport,
    nightlife,
    nature,
    shopping,
  ];
}

class CuisineType {
  static const String chinese = 'chinese';
  static const String japanese = 'japanese';
  static const String korean = 'korean';
  static const String malaysian = 'malaysian';
  static const String taiwanese = 'taiwanese';
  static const String thai = 'thai';
  static const String vietnamese = 'vietnamese';
  static const String italian = 'italian';
  static const String spanish = 'spanish';
  static const String peruvian = 'peruvian';
  static const String fastFood = 'fastfood';
  static const String vegan = 'vegan';
  static const String indian = 'indian';
  static const String mexican = 'mexican';
  static const String others = 'others';
  static const String buffet = 'buffet';
  static const String hotpot = 'hotpot';

  // List of all cuisine types for easier iteration
  static const List<String> allTypes = [
    chinese,
    japanese,
    korean,
    malaysian,
    taiwanese,
    thai,
    vietnamese,
    italian,
    spanish,
    peruvian,
    fastFood,
    vegan,
    indian,
    mexican,
    others,
    buffet,
    hotpot,
  ];
}

class TransportationType {
  static const String driving = "driving";
  static const String publicTransport = "Public Transport";
}

class LocationType {
  static const String kowloon = "Kowloon";
  static const String hongkongIsland = "Hong Kong Island";
  static const String newTerritory = "New Territory";

  static const List<String> allTypes = [kowloon, hongkongIsland, newTerritory];
}
