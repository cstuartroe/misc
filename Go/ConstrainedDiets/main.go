// A "constrained diet" is a diet that intends to somewhat recreate the experience of eating a premodern peasant diet, characterized
// by a small number of whole-food ingredients, native to or historically consumed in a given geographic zone.
// The constrained diets described here don't purport to entirely faithfully recreate any actual historical diet, and at times include non-native plants, particularly
// as substitutes for similar plants that are not readily commercially available.
// I chose to cap each diet at 20 ingredients, permitting water and salt to be implicitly added as well.
// The only non-whole food components listed are bread and cheese, which have a long history of manufacture.
// Some spices, teas, and the like may just be listed in code comments due to not being calorically significant.
// All diets given are vegetarian, as I am vegetarian.

package main

import (
	"fmt"
	"math"
)

type FoodCategory string

const (
	Starch        FoodCategory = "starch"
	Oil           FoodCategory = "oil"
	Legume        FoodCategory = "legume"
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
	Calories float64

	DigestibleCarbohydrates float64
	DietaryFiber            float64
	AnimalProtein           float64
	PlantProtein            float64
	SaturatedFat            float64
	UnsaturatedFat          float64
}

type DietComponent struct {
	Food     Food
	Multiple float64
}

type Diet struct {
	Name       string
	Components []DietComponent
}

const DIET_SIZE_CAP = 20

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
	// https://www.eatthismuch.com/calories/taro-2217?a=0.9615384615384616%3A0
	TaroRoot Food = Food{
		Name:     "raw taro root",
		Unit:     Gram,
		Category: Starch,
		Calories: 1.12,

		DigestibleCarbohydrates: .22,
		DietaryFiber:            .04,
		PlantProtein:            .02,
		UnsaturatedFat:          .002,
	}
)

var (
	// https://www.kerrygoldusa.com/products/unsalted-butter/
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
		PlantProtein:            28,
		UnsaturatedFat:          8,
	}
	// https://www.wholefoodsmarket.com/365-Everyday-Value-Organic-Black/dp/B074J5TWRM?pd_rd_w=Bcli1&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=16JSV5AGT57TDSYFH67Z&pd_rd_wg=4CkT8&pd_rd_r=bcfcecc4-ce27-43fe-9834-ae7c99e07357&pd_rd_i=B074J5TWRM&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_4_t
	BlackBeans Food = Food{
		Name:     "365 Black Beans",
		Unit:     Cup,
		Category: Legume,
		Calories: 680,

		DigestibleCarbohydrates: 92,
		DietaryFiber:            32,
		PlantProtein:            44,
		UnsaturatedFat:          2,
	}
	// https://www.wholefoodsmarket.com/365-Whole-Foods-Market-Organic/dp/B084N94MDJ?pd_rd_w=Bcli1&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=16JSV5AGT57TDSYFH67Z&pd_rd_wg=4CkT8&pd_rd_r=bcfcecc4-ce27-43fe-9834-ae7c99e07357&pd_rd_i=B084N94MDJ&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_11_t
	GreenLentils Food = Food{
		Name:     "365 green lentils",
		Unit:     Cup,
		Category: Legume,
		Calories: 680,

		DigestibleCarbohydrates: 92,
		DietaryFiber:            32,
		PlantProtein:            44,
		UnsaturatedFat:          4,
	}
)

var (
	// https://www.wholefoodsmarket.com/365-Everyday-Value-Whole-Gallon/dp/B074V3XLQ2?pd_rd_w=flHY2&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=WRM0FD1KJGX9ARMB9VNY&pd_rd_wg=gLyL1&pd_rd_r=e5104c34-2f24-445f-82ee-9cf8f5f56517&pd_rd_i=B074V3XLQ2&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_60_t
	WholeMilk Food = Food{
		Name:     "365 whole milk",
		Unit:     Cup,
		Category: AnimalProduct,
		Calories: 150,

		DigestibleCarbohydrates: 12,
		AnimalProtein:           8,
		SaturatedFat:            5,
		UnsaturatedFat:          3,
	}
	// https://www.wholefoodsmarket.com/VITAL-FARMS-Large-Grade-Eggs/dp/B0785XTLFZ?pd_rd_w=ZzeVn&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=GC5Y7QDPHDVZDY656J9K&pd_rd_wg=uKebL&pd_rd_r=7052f363-8ac5-4daf-b340-fb73ec724ac9&pd_rd_i=B0785XTLFZ&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_1_t
	Egg Food = Food{
		Name:     "Vital Farms large egg",
		Unit:     Each,
		Category: AnimalProduct,
		Calories: 70,

		AnimalProtein:  6,
		SaturatedFat:   1.5,
		UnsaturatedFat: 3.5,
	}
	// https://www.kerrygoldusa.com/products/dubliner-cheese/
	DublinerCheese Food = Food{
		Name:     "Kerrygold dubliner cheese",
		Unit:     Gram,
		Category: AnimalProduct,
		Calories: 110 / 28,

		AnimalProtein:  7 / 28,
		SaturatedFat:   6 / 28,
		UnsaturatedFat: 3 / 28,
	}
	Honey Food = Food{
		Name:     "honey",
		Unit:     Tablespoon,
		Category: AnimalProduct,
		Calories: 64,

		DigestibleCarbohydrates: 17,
	}
	// https://foodsofnations.com/products/paneer-block-12-oz
	Paneer Food = Food{
		Name:     "Nanak paneer cube",
		Unit:     Each,
		Category: AnimalProduct,
		Calories: 90 / 5.,

		DigestibleCarbohydrates: 1 / 5.,
		AnimalProtein:           6 / 5.,
		SaturatedFat:            5 / 5.,
		UnsaturatedFat:          2 / 5.,
	}
)

var (
	// https://www.wholefoodsmarket.com/Fresh-Produce-Brands-May-Vary/dp/B07FZKXQT2?pd_rd_w=ykN6R&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=D654DKMJXP49VR31HD9V&pd_rd_wg=g7ISa&pd_rd_r=227bd290-f7d9-4a85-8a5b-06168ac23e37&pd_rd_i=B07FZKXQT2&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_33_t
	SweetPotato Food = Food{
		Name:     "medium sweet potato",
		Unit:     Each,
		Category: Vegetable,
		Calories: 112,

		DigestibleCarbohydrates: 22.1,
		DietaryFiber:            3.9,
		PlantProtein:            2.04,
		SaturatedFat:            .02,
		UnsaturatedFat:          .05,
	}
	// https://www.wholefoodsmarket.com/Fresh-Produce-Brands-May-Vary/dp/B07QV6B5WV?pd_rd_w=ykN6R&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=D654DKMJXP49VR31HD9V&pd_rd_wg=g7ISa&pd_rd_r=227bd290-f7d9-4a85-8a5b-06168ac23e37&pd_rd_i=B07QV6B5WV&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_36_t
	// https://www.wholefoodsmarket.com/Fresh-Produce-Brands-May-Vary/dp/B0787Y45SB?pd_rd_w=ykN6R&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=D654DKMJXP49VR31HD9V&pd_rd_wg=g7ISa&pd_rd_r=227bd290-f7d9-4a85-8a5b-06168ac23e37&pd_rd_i=B0787Y45SB&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_40_t
	Onion Food = Food{
		Name:     "onion",
		Unit:     Each,
		Category: Vegetable,
		Calories: 96,

		DigestibleCarbohydrates: 3 * 5.6,
		DietaryFiber:            3 * 1.4,
		PlantProtein:            3 * .88,
		SaturatedFat:            3 * .03,
		UnsaturatedFat:          3 * .05,
	}
	// https://www.wholefoodsmarket.com/Produce-Brands-May-Vary-B001PLETDC/dp/B001PLETDC?pd_rd_w=ykN6R&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=D654DKMJXP49VR31HD9V&pd_rd_wg=g7ISa&pd_rd_r=227bd290-f7d9-4a85-8a5b-06168ac23e37&pd_rd_i=B001PLETDC&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_42_t
	Cucumber Food = Food{
		Name:     "cucumber",
		Unit:     Each,
		Category: Vegetable,
		Calories: 16,

		DigestibleCarbohydrates: 3.3,
		DietaryFiber:            .5,
		PlantProtein:            .68,
		SaturatedFat:            .11,
	}
	// https://www.wholefoodsmarket.com/Amazon-Fresh-Produce-Aisle-0000000940887/dp/B000RGYJQI?pd_rd_w=ykN6R&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=D654DKMJXP49VR31HD9V&pd_rd_wg=g7ISa&pd_rd_r=227bd290-f7d9-4a85-8a5b-06168ac23e37&pd_rd_i=B000RGYJQI&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_46_t
	RedBellPepper Food = Food{
		Name:     "red bell pepper",
		Unit:     Each,
		Category: Vegetable,
		Calories: 46,

		DigestibleCarbohydrates: 5.9,
		DietaryFiber:            3.1,
		PlantProtein:            1.475,
		SaturatedFat:            .04,
		UnsaturatedFat:          .41,
	}
	// https://www.wholefoodsmarket.com/Fresh-Produce-Brands-May-Vary/dp/B000P6G0GM?pd_rd_w=ykN6R&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=D654DKMJXP49VR31HD9V&pd_rd_wg=g7ISa&pd_rd_r=227bd290-f7d9-4a85-8a5b-06168ac23e37&pd_rd_i=B000P6G0GM&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_61_t
	Cauliflower Food = Food{
		Name:     "cauliflower",
		Unit:     Each,
		Category: Vegetable,
		Calories: 3.5 * 13,

		DigestibleCarbohydrates: 3.5 * 1.6,
		DietaryFiber:            3.5 * 1.1,
		PlantProtein:            3.5 * 1,
		SaturatedFat:            3.5 * .07,
		UnsaturatedFat:          3.5 * .08,
	}
	RomaTomato Food = Food{
		Name:     "roma tomato",
		Unit:     Each,
		Category: Vegetable,
		Calories: 11,

		DigestibleCarbohydrates: 2,
		DietaryFiber:            1,
		PlantProtein:            1,
		UnsaturatedFat:          .1,
	}
	// https://www.wholefoodsmarket.com/Produce-Brands-May-Vary-B001PLGQPQ/dp/B001PLGQPQ?pd_rd_w=ykN6R&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=D654DKMJXP49VR31HD9V&pd_rd_wg=g7ISa&pd_rd_r=227bd290-f7d9-4a85-8a5b-06168ac23e37&pd_rd_i=B001PLGQPQ&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_97_t
	Eggplant Food = Food{
		Name:     "eggplant",
		Unit:     Each,
		Category: Vegetable,
		Calories: 3 * 21,

		DigestibleCarbohydrates: 2.3,
		DietaryFiber:            2.5,
		PlantProtein:            .804,
		SaturatedFat:            .03,
		UnsaturatedFat:          .12,
	}
	// https://calorganicfarms.com/products/lacinato-kale/
	LacinatoKale Food = Food{
		Name:     "Cal Organic Farms lacinato kale bundle",
		Unit:     Each,
		Category: Vegetable,
		Calories: 20,

		DigestibleCarbohydrates: 3,
		DietaryFiber:            1,
		PlantProtein:            2,
	}
	Fennel Food = Food{
		Name:     "fennel bulb",
		Unit:     Each,
		Category: Vegetable,
		Calories: 72.8,

		DigestibleCarbohydrates: 10,
		DietaryFiber:            7.2,
		PlantProtein:            2.91,
		UnsaturatedFat:          .47,
	}
	Parsnip Food = Food{
		Name:     "parsnip root",
		Unit:     Each,
		Category: Vegetable,
		Calories: 100,

		DigestibleCarbohydrates: 17.5,
		DietaryFiber:            6.5,
		PlantProtein:            1.5,
		UnsaturatedFat:          .5,
	}
	AcornSquash Food = Food{
		Name:     "acorn squash",
		Unit:     Gram,
		Category: Vegetable,
		Calories: 115 / 205.,

		DigestibleCarbohydrates: 20.9 / 205.,
		DietaryFiber:            9 / 205.,
		PlantProtein:            2.3 / 205.,
	}
	RedBeet Food = Food{
		Name:     "red beet",
		Unit:     Gram,
		Category: Vegetable,
		Calories: .43,

		DigestibleCarbohydrates: .068,
		DietaryFiber:            .028,
		PlantProtein:            .016,
		UnsaturatedFat:          .002,
	}
	GreenCabbage Food = Food{
		Name:     "green cabbage",
		Unit:     Gram,
		Category: Vegetable,
		Calories: 22 / 89.,

		DigestibleCarbohydrates: 3.0 / 89.,
		DietaryFiber:            2.2 / 89.,
		PlantProtein:            1.1 / 89.,
		UnsaturatedFat:          .1 / 89.,
	}
	MustardGreens Food = Food{
		Name:     "mustard greens",
		Unit:     Cup,
		Category: Vegetable,
		Calories: 15,

		DigestibleCarbohydrates: 1,
		DietaryFiber:            2,
		PlantProtein:            2,
	}
	Okra Food = Food{
		Name:     "okra",
		Unit:     Cup,
		Category: Vegetable,
		Calories: 33,

		DigestibleCarbohydrates: 4,
		DietaryFiber:            3,
		PlantProtein:            2,
	}
	Avocado Food = Food{
		Name:     "avocado",
		Unit:     Each,
		Category: Vegetable,
		Calories: 322,

		DigestibleCarbohydrates: 3,
		DietaryFiber:            14,
		PlantProtein:            4,
		SaturatedFat:            4,
		UnsaturatedFat:          26,
	}
	// https://www.wholefoodsmarket.com/Corn-4-Count-CT/dp/B07VLMMG6R?pd_rd_w=Ql4OY&content-id=amzn1.sym.955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_p=955e5ab9-587c-4014-9ba7-267e0419b51c&pf_rd_r=7P6FZSH6ADHKA312N5SG&pd_rd_wg=Jp3SW&pd_rd_r=6fadfcc8-e58d-4172-ab49-741810e5dbf4&pd_rd_i=B07VLMMG6R&fpw=alm&almBrandId=VUZHIFdob2xlIEZvb2Rz&ref_=pd_alm_wf_dsk_cp_ai_rzg_1_77_t
	SweetCorn Food = Food{
		Name:     "sweet corn ear",
		Unit:     Each,
		Category: Vegetable,
		Calories: 87.72,

		DigestibleCarbohydrates: 17.034,
		DietaryFiber:            2.04,
		PlantProtein:            3.335,
		SaturatedFat:            1.045,
		UnsaturatedFat:          .332,
	}
	AmaranthGreens Food = Food{
		Name:     "amaranth greens",
		Unit:     Cup,
		Category: Vegetable,
		Calories: 27.72,

		DigestibleCarbohydrates: 3,
		DietaryFiber:            3,
		PlantProtein:            3,
		UnsaturatedFat:          .1,
		SaturatedFat:            .1,
	}
)

var (
	GrannySmithApple Food = Food{
		Name:     "granny smith apple",
		Unit:     Each,
		Category: Fruit,
		Calories: 97,

		DigestibleCarbohydrates: 18,
		DietaryFiber:            4.7,
		PlantProtein:            .73,
		UnsaturatedFat:          .32,
	}
	Banana Food = Food{
		Name:     "banana",
		Unit:     Each,
		Category: Fruit,
		Calories: 105,

		DigestibleCarbohydrates: 24,
		DietaryFiber:            3,
		PlantProtein:            1.29,
		UnsaturatedFat:          .39,
	}
	Papaya Food = Food{
		Name:     "papaya",
		Unit:     Gram,
		Category: Fruit,
		Calories: 62 / 145.,

		DigestibleCarbohydrates: 13.5 / 145.,
		DietaryFiber:            2.5 / 145.,
		PlantProtein:            .7 / 145.,
		UnsaturatedFat:          .4 / 145.,
	}
)

var (
	Vinegar Food = Food{
		Name:     "Trader Giotto's white modena vinegar",
		Unit:     Tablespoon,
		Category: Acid,
		Calories: 15,

		DigestibleCarbohydrates: 3,
	}
)

var (
	GingerRoot Food = Food{
		Name:     "ginger root",
		Unit:     Gram,
		Category: Spice,
		Calories: 9. / 11,

		DigestibleCarbohydrates: 1.8 / 11,
		DietaryFiber:            .2 / 11,
		PlantProtein:            .2 / 11,
	}
)

var (
	Irish Diet = Diet{
		Name: "Vaguely medieval Irish constrained diet",
		Components: []DietComponent{
			{MestemacherRye, 3.5},
			{SteelCutOats, 1},
			{UnsaltedButter, 2},
			{GreenPeas, .25},
			{FavaBeans, .25},
			{WholeMilk, 1},
			{Egg, 2},
			{DublinerCheese, 28},
			{Honey, 1},
			{Parsnip, .5},
			{RedBeet, 75},
			{LacinatoKale, .5},
			{Onion, 1},
			{GreenCabbage, 150},
			{GrannySmithApple, 1},
			{Vinegar, 1},
			{GingerRoot, 10},
			// Black pepper
			// Sage
			// Thyme
		},
	}
	Nepali Diet = Diet{
		Name: "Vaguely Nepali constrained diet",
		Components: []DietComponent{
			{BrownRice, 1},
			{TaroRoot, 600},
			{CanolaOil, 3}, // Canola is a substitute for mustard oil, which is regulated in the US for high levels of erucic acid.
			{GreenLentils, .25},
			{Chickpeas, .5},
			{Egg, 2},
			{Paneer, 5},
			{Cauliflower, .25},
			{Eggplant, .5},
			{Onion, 1},
			{MustardGreens, 1},
			{Okra, .5},
			{Banana, 2},
			{GingerRoot, 10},
			// Cumin
			// Garlic
			// Turmeric
			// Mustard
			// Coriander
			// Cardamom
		},
	}
	Mesoamerican Diet = Diet{
		Name: "Vaguely mesoamerican constrained diet",
		Components: []DietComponent{
			{Cornmeal, 1},
			{CornTortillas, 12},
			{AvocadoOil, 2},
			{BlackBeans, .5},
			{Egg, 2},
			{RomaTomato, 2},
			{Avocado, .5},
			{AcornSquash, 300},
			{RedBellPepper, 1},
			{SweetCorn, 1},
			{Onion, 1},          // Onion and garlic are not native to the Americas, but various other Allium species, difficult to commercially obtain, were consumed by pre-Columbian Americans
			{AmaranthGreens, 1}, // Also difficult to obtain at US grocery stores; may be substituted with another leafy vegetable
			{SweetPotato, 1},
			// Garlic
			// Chili pepper
			// Hoja santa
			// Cocoa powder
			// Lime
			{Papaya, 145},
			// Hibiscus
		},
	}
)

func printDietReport(diet Diet) {
	totalCalories := 0.
	var totalCarbs, totalFiber, totalAProtein, totalPProtein, totalSatFat, totalUnsatFat float64

	fmt.Println(diet.Name)
	fmt.Println()

	for _, component := range diet.Components {
		calories := component.Food.Calories * component.Multiple
		fmt.Printf("%.2f %ss of %s: %.2f calories\n", component.Multiple, component.Food.Unit, component.Food.Name, calories)
		totalCalories += calories

		totalCarbs += component.Food.DigestibleCarbohydrates * component.Multiple
		totalFiber += component.Food.DietaryFiber * component.Multiple
		totalAProtein += component.Food.AnimalProtein * component.Multiple
		totalPProtein += component.Food.PlantProtein * component.Multiple
		totalSatFat += component.Food.SaturatedFat * component.Multiple
		totalUnsatFat += component.Food.UnsaturatedFat * component.Multiple
	}

	fmt.Println()

	fmt.Printf("Total calories: %.2f\n", totalCalories)
	fmt.Printf("Total digestible carbs: %.2f\n", totalCarbs)
	fmt.Printf("Total dietary fiber: %.2f\n", totalFiber)
	fmt.Printf("Total animal protein: %.2f\n", totalAProtein)
	fmt.Printf("Total plant protein: %.2f\n", totalPProtein)
	fmt.Printf("Total saturated fat: %.2f\n", totalSatFat)
	fmt.Printf("Total unsaturated fat: %.2f\n", totalUnsatFat)

	fmt.Println()

	totalCaloriesCheck := 0.
	for _, category := range []FoodCategory{Starch, Oil, Legume, AnimalProduct, Vegetable, Fruit, Acid, Condiment, Spice, Tea} {
		categoryCalories := 0.
		for _, component := range diet.Components {
			if component.Food.Category == category {
				categoryCalories += component.Food.Calories * component.Multiple
			}
		}
		if categoryCalories != 0 {
			fmt.Printf("Calories from %s: %.2f\n", category, categoryCalories)
		}
		totalCaloriesCheck += categoryCalories
	}

	if math.Round(totalCaloriesCheck) != math.Round(totalCalories) {
		fmt.Printf("Mismatch!!!! %.2f != %.2f\n", totalCaloriesCheck, totalCalories)
	}
	if len(diet.Components) > DIET_SIZE_CAP {
		fmt.Printf("\nDiet with %d components exceeds max size of %d\n", len(diet.Components), DIET_SIZE_CAP)
	} else if len(diet.Components) < DIET_SIZE_CAP {
		fmt.Printf("\nHave room to add %d more components to this diet\n", DIET_SIZE_CAP-len(diet.Components))
	}
	fmt.Println("----------------------------------------------------------------------------")
}

func main() {
	printDietReport(Irish)
	printDietReport(Nepali)
	printDietReport(Mesoamerican)
}
