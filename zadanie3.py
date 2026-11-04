import os

class ETL:
    def __init__(self, filename_in="latest.txt", filename_out_values="values.csv", filename_out_missing="missing.values.csv"):
        self.filename_in = filename_in
        self.filename_out_values = filename_out_values
        self.filename_out_missing = filename_out_missing

    def extract(self):
        with open(file=self.filename_in, mode="rt", encoding="utf-8") as f:
            for line in f:
                yield line.rstrip()
   
    def transform(self, lines):
        for line in lines:
            row = line.split(",")
            row_id = int(row[0])
            row_sum = sum(0 if field == "-" else float(field) for field in row[1:])
            row_avg = row_sum / len(row[1:])
            row_missing_indices = [i for i, field in enumerate(row[1:], 1) if field == "-"]
            yield [row_id, row_sum, row_avg, row_missing_indices]

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