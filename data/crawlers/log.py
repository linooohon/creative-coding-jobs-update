import logging

class Log():
    logging.basicConfig(
        filename='app-basic.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    def clean_log(self):
        with open(f"./app-basic.log", "w") as f:
            pass
