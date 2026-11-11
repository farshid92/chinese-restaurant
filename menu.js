// Lucky Lid menu and restaurant details. Edit this file to change what the site sells.
//
// Each section has a name and a list of dishes.
// Each dish is: [image id, name, price in dollars, short description]
// The image id is the file name in the assets folder without ".webp".
// kind says what the dish is packed in: 'box' (default), 'tray' (the sushi drawer box) or 'cup' (tea).

window.MENU = [
  { name: 'Dumplings', items: [
    ['har-gow', 'Har Gow', 8, 'Crystal shrimp dumplings'],
    ['siu-mai', 'Siu Mai', 7, 'Open-top pork and shrimp'],
    ['jade-dumpling', 'Jade Dumpling', 7, 'Spinach skin, garden vegetables'],
    ['soup-dumpling', 'Soup Dumpling', 9, 'Xiao long bao, hot broth inside'] ] },
  { name: 'Buns', items: [
    ['char-siu-bao', 'Char Siu Bao', 7, 'Barbecue pork, split-top bun'],
    ['custard-bun', 'Lava Custard Bun', 7, 'Molten salted egg custard'],
    ['black-sesame-bun', 'Black Sesame Bun', 6, 'Roasted sesame swirl'],
    ['pan-fried-bun', 'Pan-Fried Bun', 8, 'Sheng jian bao, crisp bottom'] ] },
  { name: 'Rolls', items: [
    ['cheung-fun', 'Cheung Fun', 8, 'Rice noodle rolls, sweet soy'],
    ['spring-rolls', 'Spring Rolls', 6, 'Crisp vegetable rolls, chili dip'],
    ['lotus-rice', 'Lotus Leaf Rice', 9, 'Sticky rice, mushroom, sausage'],
    ['turnip-cake', 'Turnip Cake', 7, 'Pan-seared, golden edges'] ] },
  { name: 'Greens', items: [
    ['gai-lan', 'Gai Lan', 6, 'Chinese broccoli, oyster sauce'],
    ['bok-choy', 'Garlic Bok Choy', 6, 'Wok-tossed with golden garlic'],
    ['smashed-cucumber', 'Smashed Cucumber', 5, 'Chili, sesame, black vinegar'],
    ['wood-ear', 'Wood Ear Salad', 6, 'Black fungus, chili, coriander'] ] },
  { name: 'Sushi', kind: 'tray', items: [
    ['salmon-nigiri', 'Salmon Nigiri', 9, 'Four pieces, hand-pressed rice'],
    ['california-roll', 'California Roll', 8, 'Six pieces, crab, avocado, roe'],
    ['tuna-maki', 'Tuna Maki', 8, 'Six pieces, lean tuna'],
    ['cucumber-maki', 'Cucumber Maki', 6, 'Six pieces, crisp cucumber'] ] },
  { name: 'Sweets', items: [
    ['egg-tart', 'Egg Tart', 6, 'Flaky shell, wobbly custard'],
    ['sesame-balls', 'Sesame Balls', 6, 'Crisp, chewy, red bean heart'],
    ['mango-pudding', 'Mango Pudding', 6, 'Fresh mango, cream'],
    ['osmanthus-jelly', 'Osmanthus Jelly', 5, 'Flower tea jelly, goji'] ] },
  { name: 'Tea', kind: 'cup', items: [
    ['jasmine', 'Jasmine Pearl', 4, 'Floral, light'],
    ['pu-erh', 'Aged Pu-erh', 5, 'Dark, earthy'],
    ['oolong', 'Iron Goddess Oolong', 4, 'Toasty, smooth'],
    ['chrysanthemum', 'Chrysanthemum', 4, 'Honeyed, caffeine-free'] ] }
];

// Shown in the info panel. These are sample details for a concept site.
window.RESTAURANT = {
  tagline: 'Dim sum and sushi, steamed and rolled to order.',
  details: [
    ['Address', '12 Jade Lane, Lantern Quarter'],
    ['Hours', 'Every day, 11:00 to 22:00'],
    ['Phone', '555 0188'],
    ['Delivery', 'Within 5 km, included in the price']
  ],
  allergens: 'Dishes may contain wheat, soy, egg, sesame, fish and shellfish. Ask before ordering if you have an allergy.'
};
