from src import main


def test_main(capfd):
    main.main()
    captured = capfd.readouterr()
    assert captured.out == "hello world\n"
