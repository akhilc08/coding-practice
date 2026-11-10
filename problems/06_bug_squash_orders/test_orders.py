from solution import OrderSystem


def make():
    s = OrderSystem()
    s.add_product("pen", 150, 10)
    s.add_product("book", 1200, 3)
    s.add_product("mug", 899, 5)
    return s


def test_add_product_and_stock():
    s = make()
    assert s.add_product("pen", 1, 1) is False
    assert s.get_stock("pen") == 10
    assert s.get_stock("ghost") is None


def test_instances_are_independent():
    a = OrderSystem()
    a.add_product("x", 100, 1)
    b = OrderSystem()
    assert b.get_stock("x") is None
    assert b.add_product("x", 100, 1) is True


def test_catalog_not_mutated():
    catalog = {"x": [100, 5]}
    s = OrderSystem(catalog)
    assert s.create_order("o1", {"x": 2}) == 200
    assert catalog == {"x": [100, 5]}


def test_restock_returns_new_level():
    s = make()
    assert s.restock("pen", 5) == 15
    assert s.get_stock("pen") == 15
    assert s.restock("ghost", 5) is None


def test_create_order_total_and_stock():
    s = make()
    assert s.create_order("o1", {"pen": 2, "book": 1}) == 300 + 1200
    assert s.get_stock("pen") == 8
    assert s.get_stock("book") == 2
    assert s.get_total("o1") == 1500


def test_create_order_rejects_duplicates_and_empty():
    s = make()
    s.create_order("o1", {"pen": 1})
    assert s.create_order("o1", {"pen": 1}) is None
    assert s.create_order("o2", {}) is None
    assert s.get_stock("pen") == 9


def test_create_order_is_all_or_nothing():
    s = make()
    assert s.create_order("o1", {"pen": 2, "book": 99}) is None
    assert s.get_stock("pen") == 10
    assert s.create_order("o2", {"mug": 1, "ghost": 1}) is None
    assert s.get_stock("mug") == 5
    assert s.get_total("o1") is None


def test_order_unaffected_by_caller_mutation():
    s = make()
    items = {"pen": 1}
    s.create_order("o1", items)
    items["pen"] = 9
    assert s.cancel_order("o1") is True
    assert s.get_stock("pen") == 10


def test_coupon_basic():
    s = make()
    s.add_coupon("TEN", 10, 0)
    assert s.add_coupon("TEN", 50, 0) is False
    s.create_order("o1", {"book": 1})
    assert s.apply_coupon("o1", "TEN") == 1080
    assert s.get_total("o1") == 1080


def test_coupon_rounds_discount_down():
    s = make()
    s.add_coupon("P15", 15, 0)
    s.create_order("o1", {"mug": 1})          # 899 * 15 / 100 = 134.85 -> 134
    assert s.apply_coupon("o1", "P15") == 765
    s.add_coupon("HALF", 50, 0)
    s.create_order("o2", {"mug": 1})          # 449.5 -> 449
    assert s.apply_coupon("o2", "HALF") == 450


def test_coupon_min_total_inclusive():
    s = make()
    s.add_coupon("BIG", 20, 1200)
    s.create_order("o1", {"book": 1})          # exactly 1200
    assert s.apply_coupon("o1", "BIG") == 960
    s.create_order("o2", {"mug": 1})           # 899 < 1200
    assert s.apply_coupon("o2", "BIG") is None
    assert s.get_total("o2") == 899


def test_coupon_rejections():
    s = make()
    s.add_coupon("A", 10, 0)
    s.add_coupon("B", 10, 0)
    s.create_order("o1", {"book": 1})
    assert s.apply_coupon("ghost", "A") is None
    assert s.apply_coupon("o1", "NOPE") is None
    assert s.apply_coupon("o1", "A") == 1080
    assert s.apply_coupon("o1", "B") is None
    s.create_order("o2", {"pen": 1})
    s.cancel_order("o2")
    assert s.apply_coupon("o2", "A") is None


def test_cancel_restores_stock_once():
    s = make()
    s.create_order("o1", {"pen": 4})
    assert s.cancel_order("o1") is True
    assert s.get_stock("pen") == 10
    assert s.cancel_order("o1") is False
    assert s.get_stock("pen") == 10
    assert s.cancel_order("ghost") is False


def test_top_products():
    s = make()
    s.restock("book", 10)
    s.create_order("o1", {"pen": 3, "book": 1})
    s.create_order("o2", {"mug": 3, "book": 2})
    assert s.top_products(10) == ["book(3)", "mug(3)", "pen(3)"]
    s.create_order("o3", {"pen": 1})
    assert s.top_products(2) == ["pen(4)", "book(3)"]


def test_top_products_excludes_cancelled():
    s = make()
    s.create_order("o1", {"pen": 5})
    s.create_order("o2", {"mug": 2})
    s.cancel_order("o1")
    assert s.top_products(5) == ["mug(2)"]
