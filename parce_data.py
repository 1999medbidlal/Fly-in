from typing import List, Dict, Tuple, Any


class meta_zone:

    def __init__(self,
                 type_zone: str = "normal",
                 color_zone: str | None = None,
                 max_drones: int = 1):
        self.type_zone = type_zone
        self.color_zone = color_zone
        self.max_drones = max_drones


class Zone(meta_zone):

    def __init__(self, name: str, x: int, y: int, type_zone: str,
                 color_zone: str | None, max_drones: int):
        self.name = name
        self.x = x
        self.y = y
        super().__init__(type_zone, color_zone, max_drones)


class Connection:

    def __init__(self, zone1: str, zone2: str, max_link: int):
        self.zone1 = zone1
        self.zone2 = zone2
        self.max_link = max_link


class Parce_Data:

    def __init__(self) -> None:
        self.nb_drones: int = 0
        self.start_hub: Zone | None = None
        self.end_hub: Zone | None = None
        self.hub: Dict[str, Zone] = {}
        self.connections: List[Connection] = []

    def read_file(self, path: str) -> List[str]:
        try:
            with open(path, "r") as f:
                file: List[str] = f.readlines()
                return file
        except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
            raise Exception(f"Error: {type(e).__name__}: {e}")

    def parce_meta_data(self, valid_line: str,
                        available_keys: List[str]) -> Dict[str, Any]:
        rest_clean: Dict[str, Any] = {}
        allowed_zone = ['normal', 'blocked', 'restricted', 'priority']

        if '[' not in valid_line and ']' not in valid_line:
            return {}
        if '[' not in valid_line or ']' not in valid_line:
            raise ValueError("Unexpected format metadata brackets")
        if valid_line.split("]", 1)[1].strip():
            raise ValueError("Unexpected text after metadata brackets")
        j = valid_line.find('[')
        e = valid_line.find(']')
        data = valid_line[j + 1:e]
        if not data:
            raise ValueError("metadata does not support empty brackets")
        parts = data.split()
        for p in parts:
            if '=' not in p:
                raise ValueError("Invalid metadata format Expected key=value")
            key, value = p.split('=', 1)
            if key not in available_keys:
                raise KeyError(
                    f"Forbidden or unknown metadata key:{key} not allowed")
            if key == 'zone':
                if value not in allowed_zone:
                    raise ValueError(f"Invalid zone type: {value}")
                else:
                    rest_clean[key] = value
            if key == 'color':
                if not value:
                    raise ValueError("Color does not support empty string")
                else:
                    rest_clean[key] = value
            if key == 'max_drones':
                try:
                    max_drone = int(value)
                except ValueError:
                    raise ValueError(
                        f"invalid literal for int() with base 10: '{value}'")
                if max_drone <= 0:
                    raise ValueError("max_drones must be a positive")
                else:
                    rest_clean[key] = max_drone
            if key == 'max_link_capacity':
                try:
                    max_link = int(value)
                except ValueError:
                    raise ValueError(
                        f"invalid literal for int() with base 10: '{value}'")
                if max_link <= 0:
                    raise ValueError("max_drones must be a positive")
                else:
                    rest_clean[key] = max_link

        return rest_clean

    def validation_line(
            self,
            line: str,
            keys: List[str],
            connection: int = 0
    ) -> Tuple[str, Tuple[int, int], Dict[str, Any]]:

        valid_line = line.split("#", 1)[0].strip()
        meta_res = self.parce_meta_data(valid_line, keys)
        i = valid_line.find(':')
        j = valid_line.find('[')
        if j == -1:
            j = len(valid_line)
        data = valid_line[i + 1:j].strip().split()
        if connection == 1:
            if '-' not in data[0]:
                raise ValueError("invalid name in connection must '-'")
            else:
                data_con = data[0].split('-', 1)
        else:
            if len(data) > 3:
                raise ValueError(
                    "Zone definition requires a name,x ,y and meta_data")

        try:
            if connection == 0:
                if '-' in data[0]:
                    raise ValueError("invalid characters in name drone")
                res = (data[0], (int(data[1]), int(data[2])), meta_res)
            else:
                res = (data_con[0], data_con[1], meta_res)

        except ValueError as e:
            raise ValueError(e)
        return res

    def parce_data(self, file: List[str]) -> None:
        flag = 0
        valid_key = ["zone", "color", "max_drones"]
        valid_connection = ["max_link_capacity"]
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
                        raise ValueError(
                            "Name: nb_drones must be 'nb_drones:'")
                elif line.startswith("nb_drones:") and self.nb_drones:
                    raise ValueError("nb_drones is  duplicated")

                elif line.startswith("start_hub:"):
                    if self.start_hub is None:
                        list_line: Tuple = self.validation_line(
                            line, valid_key)
                        name, (x, y), meta = list_line
                        z_type = meta.get('zone', 'normal')
                        z_color = meta.get('color', None)
                        z_max = meta.get('max_drones', self.nb_drones)
                        self.start_hub = Zone(name, x, y, z_type, z_color,
                                              z_max)
                    else:
                        raise ValueError("start_hub is  duplicated")
                elif line.startswith("end_hub:"):
                    if self.end_hub is None:
                        list_line: Tuple = self.validation_line(
                            line, valid_key)
                        name, (x, y), meta = list_line
                        z_type = meta.get('zone', 'normal')
                        z_color = meta.get('color', None)
                        z_max = meta.get('max_drones', self.nb_drones)
                        self.end_hub = Zone(name, x, y, z_type, z_color, z_max)
                    else:
                        raise ValueError("end_hub is  duplicated")
                
                elif line.startswith("hub:"):
                    list_line: Tuple = self.validation_line(line, valid_key)
                    name, (x, y), meta = list_line
                    z_type = meta.get('zone', 'normal')
                    z_color = meta.get('color', None)
                    z_max = meta.get('max_drones', 1)
                    self.hub[name] = Zone(name, x, y, z_type, z_color, z_max)
                
                elif line.startswith("connection:"):
                    list_line: Tuple = self.validation_line(
                        line, valid_connection, 1)
                    zone1, zone2, meta = list_line
                    max_link = meta.get('max_link_capacity', 1)
                    self.connections.append(Connection(zone1, zone2, max_link))
                else:
                    raise ValueError(
                        f"Unknown line format or invalid prefix: '{line.split()[0]}'"
                    )
            except Exception as e:
                raise Exception(
                    f"Error in line {line_nb}: {type(e).__name__}: {e}")


try:
    p = Parce_Data()
    file = p.read_file("maps/challenger/01_the_impossible_dream.txt")
    p.parce_data(file)
    for k, v in p.hub.items():
        print(k)
except Exception as e:
    print(e)

# dupplacated zon
# dupplicated coordination
# IF COLORE NOT DEFFINE PICK THE DEFAULT ONE

# START AND THE END MUST BE ALWALYS MAX_DRONE
