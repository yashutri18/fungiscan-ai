"""
FungiScan AI - Expanded Specialized Fungal Disease Knowledge Base
Contains 14 common agricultural and horticultural fungal pathologies, diagnostic markers, 
susceptible host plants, characteristic foliar symptoms, and actionable prevention & remediation strategies.
"""

DISEASE_KNOWLEDGE = {
    "Early Blight": {
        "scientific_name": "Alternaria solani",
        "category": "Ascomycete Fungus",
        "species": "Tomato, Potato, Eggplant, Bell Pepper",
        "urgency": "Moderate to High",
        "symptoms": [
            "Concentric target-board ring patterns (bullseye lesions) on older lower leaves",
            "Yellow chlorotic halos surrounding dark brown necrotic spots",
            "Collar rot / sunken dark brown cankers at the soil level of mature stems",
            "Progressive bottom-to-top foliar yellowing and premature leaf drop"
        ],
        "prevention": [
            "Install drip irrigation or soaker hoses — foliage must remain completely dry",
            "Apply a 3-inch layer of clean straw or wood mulch to stop soil splash",
            "Prune off the lowest 12-18 inches of foliage once vines reach maturity",
            "Enforce a 3-4 year crop rotation away from all Solanaceae family crops",
            "Sanitize pruning shears between plants using 70% isopropyl alcohol"
        ],
        "treatment": "Spray bio-fungicides (Bacillus amyloliquefaciens) or copper octanoate at the very first sign of lower spotting; reapply every 7-10 days."
    },
    "Late Blight": {
        "scientific_name": "Phytophthora infestans",
        "category": "Oomycete Water Mold",
        "species": "Potato, Tomato, Pepper",
        "urgency": "CRITICAL (Rapid Regional Spread)",
        "symptoms": [
            "Irregular, pale water-soaked lesions near leaf margins that turn dark purplish-brown",
            "Delicate, cottony white fuzzy mycelial sporulation on the underside of leaves in humid conditions",
            "Rapid stem collapse turning dark brown/black within 48 to 72 hours",
            "Firm brown granular dry rot on potato tubers and greasy dark spots on tomato fruits"
        ],
        "prevention": [
            "Plant only certified disease-free seed potatoes and greenhouse-certified transplants",
            "Destroy all volunteer potato sprouts, cull piles, and wild solanaceous weeds (never compost)",
            "Space plants generously (36 inches apart) to ensure rapid leaf drying and air movement",
            "Monitor regional university Blitecast alerts during cool (15-20°C / 60-70°F) wet weather"
        ],
        "treatment": "Remove and immediately bag/incinerate infected plants. Apply preventive copper hydroxide or systemic mandipropamid to adjacent uninfected crops."
    },
    "Powdery Mildew": {
        "scientific_name": "Podosphaera / Erysiphe / Uncinula spp.",
        "category": "Biotrophic Ascomycete",
        "species": "Cucumber, Zucchini, Squash, Pumpkin, Grapevine, Rose, Strawberry, Apple",
        "urgency": "Moderate",
        "symptoms": [
            "Talcum-powder-like white or grayish powdery patches on upper leaf surfaces",
            "Foliage distortion, upward leaf cupping/curling, and brittle dry leaf textures",
            "Stunted flower and fruit development; premature defoliation exposing crops to sunscald"
        ],
        "prevention": [
            "Locate plantings in spots receiving at least 6-8 hours of direct, unfiltered sunlight",
            "Select resistant cultivars bred with genetic PMR (Powdery Mildew Resistance)",
            "Thin interior vegetative canopy to maximize air circulation through dense vines",
            "Avoid high-nitrogen fertilizers which force tender, ultra-susceptible young foliage"
        ],
        "treatment": "Spray potassium bicarbonate (3 tbsp/gal with Castile soap) or 40% milk / 60% water spray under direct sunlight; use wettable sulfur preventatively."
    },
    "Septoria Leaf Spot": {
        "scientific_name": "Septoria lycopersici",
        "category": "Coelomycete Fungus",
        "species": "Tomato, Tomatillo, Nightshade family",
        "urgency": "Moderate to High",
        "symptoms": [
            "Dozens of small circular spots (1.5-3mm) initially covering bottom leaves",
            "Distinct ash-gray or tan centers sharply bordered by dark brown or black margins",
            "Pinpoint black fruiting bodies (pycnidia) clearly visible inside the tan centers",
            "Rapid yellowing of the entire leaf followed by progressive leaf drop leaving bare stems"
        ],
        "prevention": [
            "Water exclusively at soil level; never handle or harvest crops when foliage is wet",
            "Thoroughly clean up and incinerate or bag all autumn tomato vines and leaf debris",
            "Stake, cage, or trellis plants to keep all foliage elevated off the ground",
            "Enforce a 2-3 year crop rotation cycle"
        ],
        "treatment": "Apply bio-fungicides with Bacillus subtilis or liquid copper fungicide at 7-10 day intervals during rainy spells."
    },
    "Leaf Rust": {
        "scientific_name": "Puccinia / Uromyces spp.",
        "category": "Basidiomycete Rust",
        "species": "Beans, Corn/Maize, Wheat, Roses, Coffee, Turfgrass",
        "urgency": "Moderate",
        "symptoms": [
            "Tiny chlorotic yellow flecks on upper leaf surfaces",
            "Prominent raised cinnamon-brown, brick-red, or golden-orange pustules on leaf undersides",
            "Powdery rust-colored spores that easily brush off onto fingers or clothing",
            "Leaves turn chlorotic, curl, wither, and prematurely drop, cutting yield severely"
        ],
        "prevention": [
            "Plant certified rust-resistant crop seed varieties",
            "Remove and destroy all crop residues and dead foliage at the end of harvest season",
            "Space plant rows widely to prevent stagnant humid microclimates around leaves",
            "Irrigate early in the morning so foliage dries quickly in the daytime sun"
        ],
        "treatment": "Dust with micronized wettable sulfur at the very first sighting of yellow speckling; use azoxystrobin or myclobutanil for ornamental or severe agricultural cases."
    },
    "Downy Mildew": {
        "scientific_name": "Pseudoperonospora cubensis / Peronospora spp.",
        "category": "Oomycete Pathogen",
        "species": "Cucumber, Cantaloupe, Melon, Grape, Basil, Spinach, Lettuce",
        "urgency": "High",
        "symptoms": [
            "Angular, polygonal chlorotic yellow patches sharply bounded by major leaf veins on top",
            "Purplish-gray, brownish downy or felt-like sporulation on the leaf underside directly below the yellow spots",
            "Leaf margins curl upwards giving foliage a crisp 'burned' or 'scorched' look"
        ],
        "prevention": [
            "Grow climbing vines vertically on trellises to keep foliage high and aerated",
            "Irrigate only at sunrise so the sun evaporates droplets before spores germinate",
            "Select downy-mildew-tolerant crop varieties",
            "Maintain generous intra-row spacing"
        ],
        "treatment": "Apply phosphonate systemic fungicides (potassium salts of phosphorous acid) or fixed copper fungicides before periods of high humidity and rainfall."
    },
    "Black Spot": {
        "scientific_name": "Diplocarpon rosae",
        "category": "Ascomycete Fungus",
        "species": "Roses (Rosa spp.), Rosaceae ornamentals",
        "urgency": "Moderate",
        "symptoms": [
            "Circular black spots (up to 12mm across) with characteristic fringed or feathery edges",
            "Tissue immediately surrounding the spots turns bright chlorotic yellow",
            "Rapid defoliation progressing upwards until canes are almost completely bare",
            "Raised dark purple or black blisters on young green canes"
        ],
        "prevention": [
            "Irrigate roses strictly with drip emitters; keep foliage dry",
            "Prune back crossing branches to open up the center of the bush for ventilation",
            "Rake up and discard every fallen infected leaf (never leave overwintering leaf litter)",
            "Plant resistant rose cultivars (e.g., shrub or landscape roses)"
        ],
        "treatment": "Spray neem oil or sulfur-based rose spray every 7-14 days; use tebuconazole or trifloxystrobin for stubborn infections on prized ornamentals."
    },
    "Anthracnose": {
        "scientific_name": "Colletotrichum spp.",
        "category": "Ascomycete Fungus",
        "species": "Tomato, Pepper, Bean, Strawberry, Mango, Cucumber, Dogwood",
        "urgency": "High (Fruit & Foliar Damage)",
        "symptoms": [
            "Small water-soaked or yellowish foliar lesions that expand into dark brown necrotic spots",
            "Sunken circular, water-soaked target-like spots on fruits with salmon-pink or orange gelatinous spore masses in the center during moist weather",
            "Shot-hole appearance when dead foliar centers crack and fall out",
            "Dieback of twigs and leaf stems"
        ],
        "prevention": [
            "Use only certified disease-free seeds (many anthracnose strains are seed-borne)",
            "Avoid harvesting or working in fields when foliage or fruit is damp",
            "Rotate crops with non-susceptible grain or grass families for at least 3 years",
            "Apply mulch beneath plants to prevent splashing spores from crop debris"
        ],
        "treatment": "Apply preventive copper sprays or chlorothalonil starting at flower bloom and early fruit set; prune and burn infected branches."
    },
    "Botrytis Gray Mold": {
        "scientific_name": "Botrytis cinerea",
        "category": "Necrotrophic Ascomycete",
        "species": "Strawberry, Grape, Tomato, Peony, Rose, Lettuce, Greenhouse crops",
        "urgency": "High (Rapid Post-Harvest Decay)",
        "symptoms": [
            "Soft, mushy water-soaked brown spots on flower petals, leaves, and ripening fruit",
            "Profuse, dense fuzzy gray-brown velvety mold coating infected tissues",
            "Flower blossoms brown prematurely and drop, failing to set fruit",
            "Girdling brown cankers on greenhouse plant stems"
        ],
        "prevention": [
            "Lower humidity in greenhouses and tunnels below 85% via active ventilation and fans",
            "Avoid overhead misting; water early in the day",
            "Prune senescing, dying leaves and faded flower petals immediately (sanitation)",
            "Chill harvested strawberries and grapes immediately after picking to 0-2°C"
        ],
        "treatment": "Apply bio-fungicide (Trichoderma harzianum or Bacillus subtilis) early in flowering; apply fenhexamid or fludioxonil where gray mold pressure is severe."
    },
    "Fusarium Wilt": {
        "scientific_name": "Fusarium oxysporum",
        "category": "Soil-Borne Vascular Ascomycete",
        "species": "Tomato, Banana, Watermelon, Melon, Basil, Cotton, Carnation",
        "urgency": "CRITICAL (Soil-Borne Vascular Collapse)",
        "symptoms": [
            "Characteristic 'one-sided wilt' — yellowing and wilting begins along one branch or one side of the plant",
            "Lower foliage turns golden yellow, wilts during the day, and fails to recover at night",
            "Internal vascular browning: brown discoloration inside the vascular xylem ring visible when stem is sliced open",
            "Complete permanent stunting, irreversible wilt, and plant death"
        ],
        "prevention": [
            "Plant resistant crop hybrids labeled 'F', 'FF', or 'FFF' (indicating resistance to Fusarium races 1, 2, or 3)",
            "Solarize garden soil with clear plastic sheets during hottest summer months for 6-8 weeks",
            "Maintain soil pH at 6.5 to 7.0 (acidic soils encourage Fusarium proliferation)",
            "Never move unsterilized soil or tools from infested fields to clean beds"
        ],
        "treatment": "No curative chemical sprays exist once vascular xylem is colonized. Pull and burn infected plants immediately; inoculate future plantings with mycorrhizae and Trichoderma biocontrols."
    },
    "Apple Scab": {
        "scientific_name": "Venturia inaequalis",
        "category": "Ascomycete Fungus",
        "species": "Apple (Malus domestica), Flowering Crabapple, Pear (Venturia pirina)",
        "urgency": "Moderate to High",
        "symptoms": [
            "Velvety olive-green to dull brown circular spots on leaf surfaces with indistinct margins",
            "Leaves become puckered, curled, and drop prematurely in mid-summer",
            "Fruit develops olive-black scabby, corky, cracked patches that deform the fruit",
            "Severe early infections cause premature June drop of tiny apples"
        ],
        "prevention": [
            "Plant scab-resistant apple cultivars (such as Liberty, Enterprise, Freedom, Pristine)",
            "Rake, chop, and compost or discard all autumn leaves to eliminate overwintering pseudothecia",
            "Prune orchard trees during winter to open up canopy structure for sunlight and wind flow",
            "Spray urea (5%) on fallen leaves in late autumn to accelerate decomposition before spring"
        ],
        "treatment": "Apply preventive captan or sulfur fungicides from tight cluster bud stage through petal fall; follow weather-based Mills infection period models."
    },
    "Cercospora Leaf Spot": {
        "scientific_name": "Cercospora spp.",
        "category": "Hyphomycete Fungus",
        "species": "Sugar Beet, Swiss Chard, Bell Pepper, Hydrangea, Soybean, Rose",
        "urgency": "Moderate",
        "symptoms": [
            "Small circular spots (2-5mm) with distinct reddish, dark purple, or brown halos",
            "Centers turn pale gray or tan and frequently dry up and drop out, creating a 'shot-hole' effect",
            "Heavily spotted leaves turn yellow, curl, dry out, and drop prematurely",
            "Under magnification, dark stomata-emerging conidiophores are visible in the gray centers"
        ],
        "prevention": [
            "Rotate out of beet, chard, or solanaceous beds for a minimum of 2-3 years",
            "Water deeply at ground level; avoid overhead sprinklers",
            "Provide ample spacing between plants for rapid morning evaporation",
            "Plow or deeply bury crop residues in autumn to accelerate fungal degradation"
        ],
        "treatment": "Apply copper-based fungicides or azoxystrobin preventatively when humidity remains high and night temperatures exceed 16°C (60°F)."
    },
    "Sooty Mold": {
        "scientific_name": "Capnodium / Scorias / Fumago spp.",
        "category": "Epiphytic Ascomycete",
        "species": "Citrus (Lemon, Orange), Hibiscus, Crepe Myrtle, Camellia, Gardenia",
        "urgency": "Low to Moderate (Non-Parasitic Epiphyte)",
        "symptoms": [
            "Dark, black or charcoal-gray soot-like powdery or crusty film coating upper leaf surfaces and stems",
            "Leaf tissue under the mold remains green and intact (the fungus does not penetrate plant tissue)",
            "Black crust blocks sunlight, impairing photosynthesis and stunting growth",
            "Sticky, shiny clear honeydew droplets present on foliage below insect infestations"
        ],
        "prevention": [
            "Control honeydew-secreting piercing-sucking insects (aphids, scale, mealybugs, whiteflies)",
            "Attract or release natural insect predators (ladybugs, lacewings, parasitic wasps)",
            "Control nuisance ants that protect aphid and scale colonies from predators",
            "Avoid planting vulnerable ornamentals beneath large honeydew-dripping trees"
        ],
        "treatment": "Wash black soot off foliage with warm water and insecticidal soap or diluted neem oil; treat the underlying sucking insects with horticultural oil."
    },
    "Healthy Foliage": {
        "scientific_name": "N/A",
        "category": "Pathogen-Free Baseline",
        "species": "All Supported Horticultural & Agricultural Crops",
        "urgency": "None (Optimum Vigor)",
        "symptoms": [
            "Uniform vibrant green pigmentation throughout lamina and margins",
            "Crisp leaf turgor, symmetrical expansion, and intact vascular venation",
            "Zero necrotic lesions, halos, powdery mats, pustules, or sooty deposits"
        ],
        "prevention": [
            "Maintain balanced biological soil fertility with rich organic compost",
            "Utilize localized drip irrigation to maintain bone-dry foliar canopies",
            "Perform scheduled bi-weekly foliar scouting of lower leaf undersides for early detection"
        ],
        "treatment": "No remedial action required. Maintain balanced feeding, proper spacing, and preventative hygiene."
    }
}