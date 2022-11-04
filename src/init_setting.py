# python manage.py shell_plus --print-sql
from label.models import * 
from django.contrib.auth.models import User

def is_debug_setting()->bool:
    return True

print("==== Start ====")

try:
    anonymous = User.objects.create_user(
            'anonymous', # user id
            'anonymous@naver.com', #user email
            'anonymous' # user pw 
            )
    anonymous.save()
    print(f"Create Anoymous : {anonymous.username}")
except:
    print("Pass to create anonymous")

# Create Test User
if is_debug_setting():
    try:
        u = User.objects.create_user(
            'tglee', # user id
            'tglee@naver.com', #user email
            'tglee1' # user pw 
            )
        u.is_staff = True
        u.is_superuser = True
        u.save()
        print(f"Create User : {u.username}")
    except:
        pass

# Create Main Category
maincategory_set = ["Overall", "Bottom", "Top", "Outer"]
attr_type_set= ["Subcategory", "Pattern", "Main Color", "Sub Color"]

attr_set={
    "Overall":{
        "Subcategory":[
            "Jumpsuit",
            "Onepiece Dress"
        ],
        "Pattern":[
            "animal", 
            "argyle", 
            "camouflage", 
            "check", 
            "dot", 
            "lettering",
            "printing", 
            "solid",
            "stripe",
            "tropical"
        ]
    },
    "Bottom":{
        "Subcategory":[
            "Jogger Pants",
            "Long Pants",
            "Long Skirt",
            "Mini Skirt",
            "Short Pants"
        ],
        "Pattern":[
            "solid",
        ]
    },
    "Top":{
        "Subcategory":[
            "Hoodie",
            "Long Sleeve Shirts",
            "Long Sleeve Tee",
            "Pullover",
            "Short Sleeve Shirts",
            "Short Sleeve Tee",
            "Sleeveless",
            "Turtleneck"
        ],
        "Pattern":[
            "animal", 
            "argyle", 
            "camouflage", 
            "check", 
            "dot", 
            "lettering",
            "printing", 
            "solid",
            "stripe",
            "tropical"
        ]
    },
    "Outer":{
        "Subcategory":[
            "Blazer Jacket",
            "Long Hoodie",
            "Long NoHood",
            "Short Blouson",
            "Short Hoodie",
            "Short None",
            "Short Normal",
            "Short Stand",
            "Vest"
        ],
        "Pattern":[
            "animal", 
            "argyle", 
            "camouflage", 
            "check", 
            "dot", 
            "lettering",
            "printing", 
            "solid",
            "stripe",
            "tropical"
        ]
    },
}
for category in maincategory_set:
    # Set Main Category
    try:
        main = Maincategory(name=category)
        main.save()
        print(f"Create {category} : "+ str(Maincategory.objects.all()))
    except Exception as ex:
        print(f"Pass {category} : " + str(ex))
        continue
        
    # Set Type category
    for attr_type in attr_type_set:
        try:
            attr_types = AttributesType(main=main, name=attr_type)
            attr_types.save()
            print(f"\tCreate {attr_type} : "+ str(AttributesType.objects.filter(main=main)))
        except Exception as ex:
            print(f"\tPass {attr_type} : " + str(ex))
            continue
        try:
            attr_list = attr_set[category][attr_type]
            print(attr_list)
        except:
            continue
        
        # Set Attributes
        for i, attr in enumerate(attr_list):
            try:
                Attributes(type=attr_types, data={"type":"class", "class":attr, "index":i}).save()
                print(f"\t\tCreate {attr} : "+ str(Attributes.objects.filter(type=attr_types)))
            except Exception as ex:
                print(f"\t\tPass {attr} : " + str(ex))
                continue

if is_debug_setting():
    attr_set={
        "Overall":{
            "Main Color":[
                list(map(lambda x: [x,x,x] ,range(0,255, 10)))
            ],
            "Sub Color":[
                list(map(lambda x: [x,x,x] ,range(0,255, 10)))
            ]
        },
        "Bottom":{
            "Main Color":[
                list(map(lambda x: [x,x,x] ,range(0,255, 10)))
            ],
            "Sub Color":[
                list(map(lambda x: [x,x,x] ,range(0,255, 10)))
            ]
        },
        "Top":{
            "Main Color":[
                list(map(lambda x: [x,x,x] ,range(0,255, 10)))
            ],
            "Sub Color":[
                list(map(lambda x: [x,x,x] ,range(0,255, 10)))
            ]
        },
        "Outer":{
            "Main Color":[
                list(map(lambda x: [x,x,x] ,range(0,255, 10)))
            ],
            "Sub Color":[
                list(map(lambda x: [x,x,x] ,range(0,255, 10)))
            ]
        },
    }
    for main_id, category in enumerate(maincategory_set):
        for attr_type in attr_type_set:
            print(f'========= {main_id} {category} : {attr_type} ================')
            try:
                attr_list = attr_set[category][attr_type]
            except:
                continue
            
            id = AttributesType.objects.get(main_id=main_id+1, name=attr_type)
            print(f"Start {id.main} {id.name}")
            
            # Set Attributes
            for attr in attr_list:
                for color in attr:
                    try:
                        attribute_color = Attributes(type=id, data={"type":"color", "color":color, "persent":50})
                        same = Attributes.objects.filter(
                            type=id,
                            data={"type":"color", "color":color, "persent":50}
                            ).first()
                        if same is None:
                            attribute_color.save()
                            print(f"Create {color} : "+ str(Attributes.objects.filter(
                                type=id,
                                data={"type":"color", "color":color, "persent":50}
                                ).first().data))
                        else:
                            pass
                    except Exception as ex:
                        print(f"\tPass {color} : " + str(ex))
                        continue
            
print("==== END ====")

        