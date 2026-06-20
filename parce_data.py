from typing import List, Dict, Tuple


class meta_zone:

    def __init__(self,
                 type_zone: str = "normal",
                 color_zone: str | None = None,
                 max_drones: int = 1):
        self.type_zone = type_zone
        self.color_zone = color_zone
        self.max_drones = max_drones


class Zone(meta_zone):

    def __init__(self,
                 name: str,
                 x: int,
                 y: int,
                 type_zone: str = "normal",
                 color_zone: str | None = None,
                 max_drones: int = 1):
        self.name = name
        self.x = x
        self.y = y
        super().__init__(type_zone, color_zone, max_drones)


class Connection:

    def __init__(self, zone1: str, zone2: str, max_link: int = 1):
        self.zone1 = zone1
        self.zone2 = zone2
        self.max_link = max_link


class Parce_Data:

    def __init__(self) -> None:
        self.nb_drones: int = 0
        self.start_hub: Zone | None = None
        self.end_hub: Zone | None = None
        self.zone: Dict[str, Zone] = {}
        self.connections: List[Connection] = []

    def read_file(self, path: str) -> List[str]:
        try:
            with open(path, "r") as f:
                file: List[str] = f.readlines()
                return file
        except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
            raise Exception(f"Error: {type(e).__name__}: {e}")

    # hub: corridorA 4 3 [zone=priority color=green max_drones=2]
    def parce_meta_data(self, data: str, avaible_keys: List[str]):
        # print(data)
        pass

    def validation_line(self, line: str) -> Tuple[str, Tuple, str]:
        comment_line = line.split("#")
        valid_line: List[str] = comment_line[0].split()
        line_str = ' '.join(valid_line)
        if line_str.split("]", 1)[1].strip():
            raise ValueError("Unexpected text after metadata brackets")
        i = line_str.find(':')
        j = line_str.find('[')
        e = line_str.find(']')
        data_zone = line_str[i + 1 : j].strip().split()
        if len(data_zone) > 3:
            raise ValueError(
                "Zone definition requires a name,x ,y and meta_data")
        else:
            try:
                if '-' in data_zone[0]:
                    raise ValueError("invalid characters in name drone")
                res = (data_zone[0], (int(data_zone[1]), int(data_zone[2])))
                print(res)
            except ValueError as e:
                raise ValueError(e)
            return res

    def parce_data(self, file: List[str]):
        flag = 0
        for line_nb, line in enumerate(file, start=1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                if flag == 0:
                    if line.startswith("nb_drones:") and self.nb_drones == 0:
                        self.nb_drones = int(line.split(":", 1)[1].strip())
                        flag = 1
                        if self.nb_drones <= 0:
                            raise ValueError("nb_drones must be a positive")
                    else:
                        raise ValueError("Name: nb_drones must be 'nb_drones'")
                elif line.startswith("nb_drones:") and self.nb_drones:
                    raise ValueError("nb_drones is  duplicated")

                elif line.startswith("start_hub:"):
                    if self.start_hub is None:
                        list_line = self.validation_line(line)
                        # meata_data = self.parce_meta_data(list_line[2], ["zone","color","max_drones"])
                        
                        
            except Exception as e:
                raise Exception(
                    f"Error in line {line_nb}: {type(e).__name__}: {e}")


p = Parce_Data()
file = p.read_file("maps/challenger/01_the_impossible_dream.txt")
try:
    p.parce_data(file)
except Exception as e:
    print(e)
