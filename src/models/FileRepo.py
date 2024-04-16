class FileRepo:
    def __init__(self, file_name: str, path: str):
        """
        Constructeur de la classe FileRepo.

        Args:
            file_name (str): Le nom du fichier.
            path (str): Le chemin du fichier.
        """
        self.__file_name = file_name
        self.__path = path
        
    def transformData2CSV(self, temps: list[int], points: list, sep: str) -> str:
        """
        Transforme les données en CSV.

        Args:
            temps (list[int]): La liste des temps.
            points (list): La liste des points.
            sep (str): Le séparateur.

        Returns:
            str: Les données au format CSV.
        """
        csv_data = "Temps" + sep + "Position X" + sep + "Position Y\n"
        for time, point in zip(temps, points):
            csv_data += f"{time}{sep}{point.getX()}{sep}{point.getY()}\n"
        return csv_data
    
    def export2CSV(self, temps: list[int], points: list, sep: str = ';') -> None:
        """
        Exporte les données au format CSV.

        Args:
            temps (list[int]): La liste des temps.
            points (list): La liste des points.
            sep (str): Le séparateur.

        Returns:
            None
        """
        csv_data = self.transformData2CSV(temps, points, sep)
        with open(f"{self.__path}/{self.__file_name}", "w") as file:
            file.write(csv_data)
