from nose.tools import assert_equal

from app.bot import Bot

command1 = {
    "command": "color",
    "data": "red"
};

command2 = {
    "command": "xxxxxxxx",
    "data": "yyyyyyyyy"
};

command3 = {
    "command": "daaaaaaaaaaaaaaaaaa",
    "data": "dl"
};

def test_bot_1():
    print("test_bot_1() <=== create a simple bot command and generate hash for command1")
    c1 = Bot(command1)
    c1.generate_hash()
    assert_equal(c1.command, "color")
    assert_equal(c1.data, "red")
    assert_equal(c1.hash, "5a2421317676")

def test_bot_2():
    print("test_bot_2() <=== create a simple bot command and generate hash for command2")
    c2 = Bot(command2)
    c2.generate_hash()
    assert_equal(c2.command, "xxxxxxxx")
    assert_equal(c2.data, "yyyyyyyyy")
    assert_equal(c2.hash, "5b92ee76ecdc285")  

def test_bot_3():
    print("test_bot_3() <=== create a simple bot command and generate hash for command3")
    c3 = Bot(command3)
    c3.generate_hash()
    assert_equal(c3.command, "daaaaaaaaaaaaaaaaaa")
    assert_equal(c3.data, "dl")
    assert_equal(c3.hash, "22cf35f16189ca")    
