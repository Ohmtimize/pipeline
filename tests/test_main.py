from src import main


def test_main(capfd):
    main.main()
    captured = capfd.readouterr()
    assert "Success" and "Disconnecting" in captured.out
    
