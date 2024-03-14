class FileRepo:
    def __init__(self, file_name, path):
        self.__file_name = file_name
        self.__path = path
        
    def transformData2CSV(self, temps: list, points: list, sep: str) -> str:
        csv_data = "Temps" + sep + "Position X" + sep + "Position Y\n"
        for time, point in zip(temps, points):
            csv_data += f"{time}{sep}{point.getX()}{sep}{point.getY()}\n"
        return csv_data
    
    def export2CSV(self, temps: list, points: list, sep: str = ';'):
        csv_data = self.transformData2CSV(temps, points, sep)
        with open(f"{self.__path}/{self.__file_name}", "w") as file:
            file.write(csv_data)
