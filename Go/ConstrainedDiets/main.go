package main

type FoodCategory string

const (
	Starch        FoodCategory = "starch"
	Legume        FoodCategory = "legume"
	Oil           FoodCategory = "oil"
	AnimalProduct FoodCategory = "animal product"
	Vegetable     FoodCategory = "vegetable"
	Fruit         FoodCategory = "fruit"
	Acid          FoodCategory = "acid"
	Condiment     FoodCategory = "condiment"
	Spice         FoodCategory = "spice"
	Tea           FoodCategory = "tea"
)

type Unit string

const (
	Teaspoon   Unit = "teaspoon"
	Tablespoon Unit = "tablespoon"
	Each       Unit = "each"
	Gram       Unit = "gram"
	Slice      Unit = "slice"
	Cup        Unit = "cup"
)

type Food struct {
	Name     string
	Unit     Unit
	Category FoodCategory
	Calories float32

	DigestibleCarbohydrates float32
	DietaryFiber            float32
	AnimalProtein           float32
	PlantProtein            float32
	SaturatedFat            float32
	UnsaturatedFat          float32
}

type DietComponent struct {
	Food     Food
	Multiple float32
}

type Diet struct {
	Name      string
	Component []DietComponent
}

var (
	// https://www.mestemacher-gmbh.com/product/whole-rye-bread-usa/#tab-id-2
	MestemacherRye Food = Food{
		Name:     "Mestemacher whole rye bread",
		Unit:     Slice,
		Category: Starch,
		Calories: 180,

		DigestibleCarbohydrates: 32,
		DietaryFiber:            8,
		PlantProtein:            4,
		UnsaturatedFat:          1,
	}
	// https://www.bobsredmill.com/product/steel-cut-oats
	SteelCutOats Food = Food{
		Name:     "Bob's Red Mill steel-cut oats",
		Unit:     Cup,
		Category: Starch,
		Calories: 680,

		DigestibleCarbohydrates: 104,
		DietaryFiber:            20,
		PlantProtein:            20,
		SaturatedFat:            2,
		UnsaturatedFat:          8,
	}
	// https://www.wholefoodsmarket.com/365-Whole-Foods-Market-Organic/dp/B084NHD2R5?pd_rd_w=qwvry&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=ZSCCPNJ57JAV1K9EH5JK&pd_rd_wg=mO2d0&pd_rd_r=1e8312d4-99ee-41d9-a749-03e94c136193&pd_rd_i=B084NHD2R5&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_41_t
	BrownRice Food = Food{
		Name:     "365 long-grain brown rice",
		Unit:     Cup,
		Category: Starch,
		Calories: 640,

		DigestibleCarbohydrates: 132,
		DietaryFiber:            4,
		PlantProtein:            12,
		UnsaturatedFat:          4,
	}
	// https://www.wholefoodsmarket.com/Produce-PRODUCE-Organic-Yellow-Potato/dp/B07PY3GQSQ?pd_rd_w=MpnSB&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=AQ6FACHPE1KFTDEWTDQE&pd_rd_wg=7bg6m&pd_rd_r=f25f65d1-0fb7-4fd3-b8ec-fd659c583a74&pd_rd_i=B07PY3GQSQ&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_62_t
	YellowPotato Food = Food{
		Name:     "yellow potato",
		Unit:     Each,
		Category: Starch,
		Calories: 164,

		DigestibleCarbohydrates: 32.5,
		DietaryFiber:            4.5,
		PlantProtein:            4.366,
		SaturatedFat:            .05,
		UnsaturatedFat:          .14,
	}
	// https://www.bobsredmill.com/product/medium-grind-cornmeal
	Cornmeal Food = Food{
		Name:     "Bob's Red Mill medium-grind cornmeal",
		Unit:     Cup,
		Category: Starch,
		Calories: 560,

		DigestibleCarbohydrates: 104,
		DietaryFiber:            16,
		PlantProtein:            12,
		UnsaturatedFat:          6,
	}
	// https://www.wholefoodsmarket.com/365-Whole-Foods-Market-Tortillas/dp/B084R4R9PK?pd_rd_w=v65Wn&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=J4J1HSVH2RHXBRVT52QY&pd_rd_wg=1ypqY&pd_rd_r=f6f5cb8d-7c00-4997-843c-4c42f541a303&pd_rd_i=B084R4R9PK&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_pc_2_1_146_t
	CornTortillas Food = Food{
		Name:     "365 corn tortillas",
		Unit:     Each,
		Category: Starch,
		Calories: 130. / 3,

		DigestibleCarbohydrates: 8,
		DietaryFiber:            1,
		PlantProtein:            1,
		UnsaturatedFat:          1. / 3,
	}
	// https://www.wholefoodsmarket.com/Angel-Bakeries-Bread-Whole-Wheat/dp/B07G5S1359?pd_rd_w=v65Wn&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=J4J1HSVH2RHXBRVT52QY&pd_rd_wg=1ypqY&pd_rd_r=f6f5cb8d-7c00-4997-843c-4c42f541a303&pd_rd_i=B07G5S1359&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_pc_2_1_223_t
	WholeWheatPita Food = Food{
		Name:     "Angel Bakeries whole wheat pita",
		Unit:     Each,
		Category: Starch,
		Calories: 220,

		DigestibleCarbohydrates: 38,
		DietaryFiber:            5,
		PlantProtein:            9,
		UnsaturatedFat:          1.5,
	}
	// https://www.wholefoodsmarket.com/365-Everyday-Value-Organic-Bulgur/dp/B074H6VRKY?pd_rd_w=H7Eo8&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=C74ND0SB9ZRXZ1T7827X&pd_rd_wg=HUzQ4&pd_rd_r=102aea52-896b-4774-9c52-0af6d4d1b59a&pd_rd_i=B074H6VRKY&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_96_t
	Bulgur Food = Food{
		Name:     "365 whole grain bulgur wheat",
		Unit:     Cup,
		Category: Starch,
		Calories: 680,

		DigestibleCarbohydrates: 108,
		DietaryFiber:            20,
		PlantProtein:            24,
		UnsaturatedFat:          6,
	}
	// https://www.bobsredmill.com/product/bulgur
	RedBulgur Food = Food{
		Name:     "Bob's Red Mill red bulgur",
		Unit:     Cup,
		Category: Starch,
		Calories: 640,

		DigestibleCarbohydrates: 120,
		DietaryFiber:            20,
		PlantProtein:            16,
		UnsaturatedFat:          2,
	}
)

var (
	UnsaltedButter Food = Food{
		Name:     "Kerrygold unsalted butter",
		Unit:     Tablespoon,
		Category: Oil,
		Calories: 100,

		SaturatedFat:   8,
		UnsaturatedFat: 4,
	}
	CanolaOil Food = Food{
		Name:     "365 canola oil",
		Unit:     Tablespoon,
		Category: Oil,
		Calories: 120,

		SaturatedFat:   1,
		UnsaturatedFat: 13,
	}
	AvocadoOil Food = Food{
		Name:     "365 avocado oil",
		Unit:     Tablespoon,
		Category: Oil,
		Calories: 130,

		SaturatedFat:   2,
		UnsaturatedFat: 12,
	}
	OliveOil Food = Food{
		Name:     "365 extra virgin olive oil",
		Unit:     Tablespoon,
		Category: Oil,
		Calories: 120,

		SaturatedFat:   2,
		UnsaturatedFat: 12,
	}
)

var (
	// https://www.bobsredmill.com/product/green-split-peas
	GreenPeas Food = Food{
		Name:     "Bob's Red Mill green split pea",
		Unit:     Cup,
		Category: Legume,
		Calories: 720,

		DigestibleCarbohydrates: 104,
		DietaryFiber:            24,
		PlantProtein:            44,
		UnsaturatedFat:          2,
	}
	// https://www.wholefoodsmarket.com/SIMPLI-Organic-Fava-Beans-12/dp/B0DYR8HBXM?pd_rd_w=Bcli1&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=16JSV5AGT57TDSYFH67Z&pd_rd_wg=4CkT8&pd_rd_r=bcfcecc4-ce27-43fe-9834-ae7c99e07357&pd_rd_i=B0DYR8HBXM&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_101_t
	FavaBeans Food = Food{
		Name:     "Simpli fava beans",
		Unit:     Cup,
		Category: Legume,
		Calories: 480,

		DigestibleCarbohydrates: 44,
		DietaryFiber:            36,
		PlantProtein:            36,
		UnsaturatedFat:          2,
	}
	// https://www.wholefoodsmarket.com/365-Whole-Foods-Market-Garbanzo/dp/B084NHQTT5?pd_rd_w=Bcli1&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=16JSV5AGT57TDSYFH67Z&pd_rd_wg=4CkT8&pd_rd_r=bcfcecc4-ce27-43fe-9834-ae7c99e07357&pd_rd_i=B084NHQTT5&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_25_t
	Chickpeas Food = Food{
		Name:     "365 garbanzo beans",
		Unit:     Cup,
		Category: Legume,
		Calories: 440,

		DigestibleCarbohydrates: 60,
		DietaryFiber:            36,
	}
)
