from typing import List, Dict, Tuple, Any


class meta_zone:
    """
    Represents the metadata configurations for a simulation zone.
    """

    def __init__(self,
                 type_zone: str = "normal",
                 color_zone: str | None = None,
                 max_drones: int = 1):
        """
        Initializes meta_zone attributes..

        Attributes:
        type_zone (str): The classification type of the zone.
        color_zone (str | None): Visual color representation.
        max_drones (int): Maximum limit of drones allowed inside
        """
        self.type_zone = type_zone
        self.color_zone = color_zone
        self.max_drones = max_drones


class Zone(meta_zone):
    """
    Represents a physical hub or zone inside the simulation map.
    """

    def __init__(self, name: str, x: int, y: int, type_zone: str,
                 color_zone: str | None, max_drones: int):
        """
        Initializes a Zone object with its coordinates and metadata.

        Attributes:
        name (str): Unique identifier name of the zone.
        x (int): X-axis coordinate.
        y (int): Y-axis coordinate.
        """
        self.name = name
        self.x = x
        self.y = y
        super().__init__(type_zone, color_zone, max_drones)


class Connection:
    """
    Represents a link between two distinct simulation zones.
    """

    def __init__(self, zone1: str, zone2: str, max_link: int):
        self.zone1 = zone1
        self.zone2 = zone2
        self.max_link = max_link
        """
        Initializes a Connection link with a maximum link capacity.

        Attributes:
        zone1 (str): Name of the first connected zone.
        zone2 (str): Name of the second connected zone.
        max_link (int): Maximum capacity flow of the connection.
        """


class Data:
    """
    Handles parsing, validation, and loading of simulation map files
    """

    def __init__(self) -> None:
        """
        Initializes container structures for parsed map attributes.

        Attributes:
        nb_drones (int): Total number of drones allowed.
        start_hub (Zone | None): Thestarting zone/hub object.
        end_hub (Zone | None): The target or goal zone/hub object.
        hub (Dict[str, Zone]): Dictionary mapping hub names.
        connections (List[Connection]): List of all validated link connection.
        """
        self.nb_drones: int = 0
        self.start_hub: Zone | None = None
        self.end_hub: Zone | None = None
        self.hub: Dict[str, Zone] = {}
        self.connections: List[Connection] = []

    def read_file(self, path: str) -> List[str]:
        """Reads content lines from a specified raw file path.

        Args:
            path (str): Target file system path.

        Returns:
            List[str]: A list of untrimmed raw strings from the file.
        """
        try:
            with open(path, "r") as f:
                file: List[str] = f.readlines()
                return file
        except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
            raise Exception(f"Error: {type(e).__name__}: {e}")

    def parce_meta_data(self, valid_line: str,
                        available_keys: List[str]) -> Dict[str, Any]:
        """
        Extracts and verifies key-value metadata parameters in brackets.

        Args:
            valid_line (str): The clean data line to extract brackets.
            available_keys (List[str]): List of allowed keys for metadata.

        Returns:
            Dict[str, Any]: Extracted metadata keys and their type-cast values.
        """
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
        line_keys = [
            key.split('=')[0].strip() for key in data.split() if '=' in key
        ]
        if len(line_keys) != len(set(line_keys)):
            raise ValueError("keys_meta_data: duplicated")
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
            connection: int = 0) -> Tuple[str, Any, Dict[str, Any]]:
        """
        Validates syntax formats for either map zones or map links connections.

        Args:
            line (str): Raw map configuration string line.
            keys (List[str]): Allowed metadata keys for this specific line.
            connection (int): Toggle flag (0 for Zone/Hub info, 1 for Connect).

        Returns:
            Tuple[str, Any, Dict[str, Any]]: Main name, parsed data details
            (coordinates tuple or second zone string), and the parsed metadata.
        """

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
                return (data[0], (int(data[1]), int(data[2])), meta_res)
            else:
                return (data_con[0], data_con[1], meta_res)

        except ValueError as e:
            raise ValueError(e)

    def parce_data(self, file: List[str]) -> None:
        """
        Processes and stores sequential map rows onto simulation structures.

        Args:
            file (List[str]): Array containing raw line content
            from the map file stream.

        Returns:
            None
        """
        flag: int = 0
        valid_key: List[str] = ["zone", "color", "max_drones"]
        valid_connection: List[str] = ["max_link_capacity"]
        zone_name: List[str] = []
        zone_coord: List[Tuple[int, int]] = []
        connections_name: List[List[str]] = []
        for line_nb, line in enumerate(file, start=1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                if flag == 0:
                    if line.startswith("nb_drones") and self.nb_drones == 0:
                        self.nb_drones = int(line.split(":", 1)[1].strip())
                        flag = 1
                        if self.nb_drones <= 0:
                            raise ValueError("nb_drones must be a positive")
                    else:
                        raise ValueError(
                            "Name: nb_drones must be 'nb_drones:'")
                elif line.startswith("nb_drones") and self.nb_drones:
                    raise ValueError("line nb_drones is  duplicated")

                elif line.startswith("start_hub"):
                    if self.start_hub is None:
                        list_line = self.validation_line(line, valid_key)
                        name, (x, y), meta = list_line
                        if name in zone_name:
                            raise ValueError("start_hub_name: duplicated")
                        if (x, y) in zone_coord:
                            raise ValueError("start_hub_coord: duplicated")
                        zone_name.append(name)
                        zone_coord.append((x, y))
                        z_type = meta.get('zone', 'normal')
                        z_color = meta.get('color', None)
                        z_max = self.nb_drones
                        self.start_hub = Zone(name, x, y, z_type, z_color,
                                              z_max)
                        self.hub[name] = Zone(name, x, y, z_type, z_color, z_max)
                    else:
                        raise ValueError("line start_hub is  duplicated")
                elif line.startswith("end_hub"):
                    if self.end_hub is None:
                        list_line = self.validation_line(line, valid_key)
                        name, (x, y), meta = list_line
                        if name in zone_name:
                            raise ValueError("end_hub_name: duplicated")
                        if (x, y) in zone_coord:
                            raise ValueError("end_hub_coord: duplicated")
                        zone_name.append(name)
                        zone_coord.append((x, y))
                        z_type = meta.get('zone', 'normal')
                        z_color = meta.get('color', None)
                        z_max = self.nb_drones
                        self.end_hub = Zone(name, x, y, z_type, z_color, z_max)
                        self.hub[name] = Zone(name, x, y, z_type, z_color, z_max)
                        
                    else:
                        raise ValueError("line end_hub is duplicated")

                elif line.startswith("hub"):
                    list_line = self.validation_line(line, valid_key)
                    name, (x, y), meta = list_line
                    if name in zone_name:
                        raise ValueError("hub_name: duplicated")
                    if (x, y) in zone_coord:
                        raise ValueError("hub_coord: duplicated")
                    zone_name.append(name)
                    zone_coord.append((x, y))
                    z_type = meta.get('zone', 'normal')
                    z_color = meta.get('color', "gray")
                    z_max = meta.get('max_drones', 1)
                    self.hub[name] = Zone(name, x, y, z_type, z_color, z_max)

                elif line.startswith("connection"):
                    list_line = self.validation_line(line, valid_connection, 1)
                    name_conz1, name_conz2, _ = list_line
                    if name_conz1 == name_conz2:
                        raise ValueError("a hub can't connect to it self")
                    current_pair = sorted([name_conz1, name_conz2])
                    if (current_pair) in connections_name:
                        raise ValueError("connection: duplicated")
                    connections_name.append(current_pair)
                    zone1, zone2, meta = list_line
                    if zone1 not in zone_name or zone2 not in zone_name:
                        raise ValueError("invalid name connection")
                    max_link = meta.get('max_link_capacity', 1)
                    self.connections.append(Connection(zone1, zone2, max_link))
                else:
                    raise ValueError("Unknown line format or invalid prefix: "
                                     f"'{line.split()[0]}'")
            except Exception as e:
                raise Exception(
                    f"Error in line {line_nb}: {type(e).__name__}: {e}")

        try:
            if self.start_hub is None:
                raise ValueError("not exist start_hub")
            if self.end_hub is None:
                raise ValueError("not exist end_hub")
        except Exception as e:
            raise Exception(
                f"Error in line {line_nb}: {type(e).__name__}: {e}")
