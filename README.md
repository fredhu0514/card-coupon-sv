.
├── Dockerfile
├── README.md
├── apis
│   ├── __init__.py
│   ├── coupon
│   │   ├── __init__.py
│   │   └── routes.py
│   └── credit_card
│       ├── __init__.py
│       └── routes.py
├── app.py
├── card-coupon-db
│   ├── development
│   │   ├── db_public.sqlite3
│   │   └── static
│   │       └── credit_card_images
│   │           ├── 10b829f909b50c66ed0b21f78bafdedd.png
│   │           ├── 46302505e98cb34f4520e1b4b0af0e71.png
│   │           ├── 47dea354faf8a00e7a0b00a05b41c1f2.png
│   │           ├── 7aa75b69bd949c498f28ce705dc059b6.png
│   │           ├── 9453384f6aa6e9f70fa1624540209f04.png
│   │           ├── a9baf94073f3aa40d22090bbbd57c0d5.png
│   │           ├── ac2f1b9c4cf8149af9e0b3fbcc49000b.png
│   │           ├── bb75dbc57aa34b652796f5289b9b3cb3.png
│   │           ├── c267b9577b2e5bcd9d660182010d4e74.png
│   │           └── ff1f0c4d86c064e3f0a7d27aad585bc7.png
│   ├── production
│   │   └── static
│   │       └── credit_card_images
│   └── testing
│       └── static
│           └── credit_card_images
├── config.py
├── dev_request
│   ├── add_coupons.py
│   ├── add_credit_cards.py
│   ├── data
│   │   ├── coupons_0.json
│   │   ├── coupons_1.json
│   │   └── credit_cards_0.json
│   ├── get_coupons.py
│   └── images
│       ├── chase_amazon.png
│       ├── chase_freedom_flex.png
│       ├── chase_freedom_rise.png
│       ├── chase_freedom_unlimited.png
│       ├── chase_prime.png
│       ├── chase_sapphire_preferred.png
│       ├── chase_sapphire_reserve.png
│       ├── citi_custom_cash.png
│       ├── citi_double_cash.png
│       └── discover_it_cash_back.png
├── docker-compose.yml
├── models
│   ├── __init__.py
│   ├── coupon.py
│   ├── credit_card.py
│   └── interfaces
│       ├── __init__.py
│       └── base_model.py
├── requirements.txt
└── tests
    ├── test_coupon_routes.py
    └── test_credit_card_routes.py