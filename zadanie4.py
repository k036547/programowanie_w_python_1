from datetime import datetime

def timestamps(func):
    def wrapper(*args, **kwargs):
        print(f"{f'Time before function \"{func.__name__}\" call:':<42}", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        result = func(*args, **kwargs)
        print(f"{f'Time after function \"{func.__name__}\" call:':<42}", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        return result
    return wrapper

def timestamps_for_generators(func):
    def wrapper(*args, **kwargs):
        print(f"{f'Time before function \"{func.__name__}\" call:':<42}", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        yield from func(*args, **kwargs)
        print(f"{f'Time after function \"{func.__name__}\" call:':<42}", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    return wrapper

class ETL:
    def __init__(self, filename_in="latest.txt", filename_out_values="values.csv", filename_out_missing="missing.values.csv"):
        self.filename_in = filename_in
        self.filename_out_values = filename_out_values
        self.filename_out_missing = filename_out_missing

    @timestamps_for_generators
    def extract(self):
        print(f"Extracting data from {self.filename_in}...")
        with open(file=self.filename_in, mode="rt", encoding="utf-8") as f:
            for line in f:
                yield line.rstrip()

    @timestamps_for_generators
    def transform(self, lines):
        for line in lines:
            row = line.split(",")
            row_id = int(row[0])
            row_sum = sum(0 if field == "-" else float(field) for field in row[1:])
            row_avg = row_sum / len(row[1:])
            row_missing_indices = [i for i, field in enumerate(row[1:], 1) if field == "-"]
            yield [row_id, row_sum, row_avg, row_missing_indices]

    @timestamps
    def load(self, entries):
        with open(file=self.filename_out_values, mode="wt", encoding="utf-8", newline="") as fov:
            with open(file=self.filename_out_missing, mode="wt", encoding="utf-8", newline="") as fom:
                for entry in entries:
                    row_id, row_sum, row_avg, row_missing_indices = entry
                    fov.write(f"{row_id}, {row_sum}, {row_avg}\n")
                    if row_missing_indices:
                        row_missing_indices_string = ", ".join(map(str, row_missing_indices))
                        fom.write(f"{row_id}, {row_missing_indices_string}\n")

if __name__ == "__main__":
    etl = ETL(filename_in="latest.txt", filename_out_values="values.csv", filename_out_missing="missing_values.csv")
    etl.load(etl.transform(etl.extract()))