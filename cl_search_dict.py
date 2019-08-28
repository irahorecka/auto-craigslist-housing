#A file to store room filters, rooming categories, and state keys in dictionaries

room_filters = {'private_room' : True, #bool
    'private_bath' : None, #bool
    'cats_ok' : None, #bool
    'dogs_ok' : None, #bool
    'min_price' : 500,
    'max_price' : 1200,
    'min_ft2' : None,
    'max_ft2' : None,
    'min_bedrooms' : None,
    'max_bedrooms' : None,
    'min_bathrooms' : None,
    'max_bathrooms' : None,
    'no_smoking' : None, #bool
    'is_furnished' : None, #bool
    'wheelchair_acccess' : None, #bool
    'has_image' : True #bool
}

cat_dict = {'apa':'apts/housing for rent',
    'swp':'housing swap',
    'off':'office & commercial',
    'prk':'parking & storage',
    'reb':'real estate - by broker',
    'reo':'real estate - by owner',
    'roo':'rooms & shares',
    'sub':'sublets & temporary',
    'vac':'vacation rentals',
    'hou':'wanted: apts',
    'rew':'wanted: real estate',
    'sha':'wanted: room/share',
    'sbw':'wanted: sublet/temp'}

apa_dict = {'aap':'apts/housing for rent',
    'swp':'housing swap',
    'off':'office & commercial',
    'prk':'parking & storage',
    'reb':'real estate - by broker',
    'reo':'real estate - by owner',
    'roo':'rooms & shares',
    'sub':'sublets & temporary',
    'vac':'vacation rentals',
    'hou':'wanted: apts',
    'rew':'wanted: real estate',
    'sha':'wanted: room/share',
    'sbw':'wanted: sublet/temp'}