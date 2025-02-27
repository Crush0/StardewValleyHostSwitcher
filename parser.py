import os
from xml.dom.minidom import parse, Element


def getElementByTagName(node: Element, tag_name: str, cloneNode : bool = False) -> Element or None:
    for element in node.getElementsByTagName(tag_name):
        if element.parentNode == node:
            return element.cloneNode(True) if cloneNode else element
    return None

class Parser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        if os.path.exists(file_path):
            self.dom = parse(file_path)
            self.save_game = self.dom.getElementsByTagName("SaveGame")[0]
        else:
            self.dom = None
            raise FileNotFoundError("File not found")


    def get_farmers(self) -> list:
        farmers = []
        farmhands = getElementByTagName(self.save_game, "farmhands")
        for farmer in farmhands.getElementsByTagName("Farmer"):
            try:
                name = getElementByTagName(farmer, "name").firstChild.nodeValue
            except AttributeError:
                name = "Unknown"
            try:
                userId = farmer.getElementsByTagName("UniqueMultiplayerID")[0].firstChild.nodeValue
            except AttributeError:
                userId = "Unknown"
            if name == "Unknown" and userId == "Unknown":
                continue
            # 深拷贝farmer
            farmers.append({"name": name, "userId": userId, "tag": farmer})
        return farmers

    def get_player(self) -> dict:
        player = getElementByTagName(self.save_game, "player")
        try:
            name = getElementByTagName(player, "name").firstChild.nodeValue
        except AttributeError:
            name = "Unknown"
        try:
            userId = getElementByTagName(player, "UniqueMultiplayerID").firstChild.nodeValue
        except AttributeError:
            userId = "Unknown"
        return {"name": name, "userId": userId, "tag": player}

    def get_player_tag(self) -> Element:
        return getElementByTagName(self.save_game, "player")

    def switch_host(self, player) -> Element:
        # 删除dom中的player节点，并保存到临时变量中
        player_tag = self.get_player_tag()
        self.save_game.removeChild(player_tag)
        # 找到新的主持人节点，并插入到dom中
        farmers = self.get_farmers()
        origin_host_home_location = getElementByTagName(player_tag, "homeLocation").firstChild.nodeValue
        new_host_home_location = None
        new_player_tag = None
        for farmer in farmers:
            # 找到新主持人节点
            if farmer["userId"] == player["userId"] and farmer["name"] == player["name"]:
                new_player_tag = farmer["tag"].cloneNode(True)
                new_host_home_location = getElementByTagName(new_player_tag, "homeLocation").firstChild.nodeValue
                # 将tag的名字改为player
                new_player_tag.tagName = "player"
                # 将tag的xml字符串插入到dom中
                self.save_game.insertBefore(new_player_tag, self.save_game.firstChild)
                # 删除farmer
                getElementByTagName(self.save_game, "farmhands").removeChild(farmer["tag"])
                # 将原来的player插入farmer中
                player_tag.tagName = "Farmer"
                getElementByTagName(self.save_game, "farmhands").appendChild(player_tag)
                break
        if new_host_home_location is not None and origin_host_home_location is not None and new_host_home_location != origin_host_home_location:
            # 将原来主持人的家园位置改为新主持人的家园位置
            getElementByTagName(player_tag, "homeLocation").firstChild.nodeValue = new_host_home_location
            # 将新主持人的家园位置改为原来的主持人的家园位置
            getElementByTagName(new_player_tag, "homeLocation").firstChild.nodeValue = origin_host_home_location
            # 将新主持人的房子的主人设置为原来的主持人
            locations = getElementByTagName(self.save_game, "locations")
            farm_house = None
            for location in locations.getElementsByTagName("GameLocation"):
                if getElementByTagName(location, "name").firstChild.nodeValue == "FarmHouse":
                    farm_house = location
                    break
            for location in locations.getElementsByTagName("GameLocation"):
                if getElementByTagName(location, "name").firstChild.nodeValue == "Farm":
                    for building in getElementByTagName(location, "buildings").getElementsByTagName("Building"):
                        indoors = building.getElementsByTagName("indoors")
                        if len(indoors) > 0:
                            indoor = indoors[0]
                            indoor_unique_name = getElementByTagName(indoor, "uniqueName").firstChild.nodeValue
                            if indoor_unique_name == new_host_home_location:
                                getElementByTagName(indoor, "farmhandReference").firstChild.nodeValue = getElementByTagName(player_tag,"UniqueMultiplayerID").firstChild.nodeValue
                                # 交换indoor和farm_house的characters节点
                                characters = getElementByTagName(indoor, "characters").cloneNode(True)
                                farm_house_characters = getElementByTagName(farm_house, "characters").cloneNode(True)
                                # 将每个characters的defaultMap节点设置为farm_house的uniqueName
                                for character in characters.childNodes:
                                    default_map_node = getElementByTagName(character, "defaultMap")
                                    if default_map_node is not None:
                                        default_map_node.firstChild.nodeValue = "FarmHouse"
                                for farm_house_character in farm_house_characters.childNodes:
                                    default_map_node = getElementByTagName(farm_house_character, "defaultMap")
                                    if default_map_node is not None:
                                        default_map_node.firstChild.nodeValue = indoor_unique_name
                                indoor.removeChild(getElementByTagName(indoor, "characters"))
                                indoor.appendChild(farm_house_characters)
                                farm_house.removeChild(getElementByTagName(farm_house, "characters"))
                                farm_house.appendChild(characters)
                                # 交换indoor和farm_house的节点
                                for change_node in ["objects", "waterColor", "furniture", "Animals", "appliedWallpaper", "appliedFloor", "fridgePosition", "fridge"]:
                                    objects = getElementByTagName(indoor, change_node).cloneNode(True)
                                    farm_house_objects = getElementByTagName(farm_house, change_node).cloneNode(True)
                                    indoor.removeChild(getElementByTagName(indoor, change_node))
                                    indoor.appendChild(farm_house_objects)
                                    farm_house.removeChild(getElementByTagName(farm_house, change_node))
                                    farm_house.appendChild(objects)
                                break
        # 将新主持人的事件记录设置为原来的主持人的事件记录
        origin_recevied_email = getElementByTagName(player_tag, "mailReceived").cloneNode(True)
        new_player_tag.removeChild(getElementByTagName(new_player_tag, "mailReceived"))
        new_player_tag.appendChild(origin_recevied_email)
        origin_event_seen = getElementByTagName(player_tag, "eventsSeen").cloneNode(True)
        new_player_tag.removeChild(getElementByTagName(new_player_tag, "eventsSeen"))
        new_player_tag.appendChild(origin_event_seen)
        # 交换原主持人和新主持人的houseUpgradeLevel
        origin_house_upgrade_level = player_tag.getElementsByTagName("houseUpgradeLevel")[0].firstChild.nodeValue
        new_house_upgrade_level = new_player_tag.getElementsByTagName("houseUpgradeLevel")[0].firstChild.nodeValue
        player_tag.getElementsByTagName("houseUpgradeLevel")[0].firstChild.nodeValue = new_house_upgrade_level
        new_player_tag.getElementsByTagName("houseUpgradeLevel")[0].firstChild.nodeValue = origin_house_upgrade_level
        # 交换原主持人和新主持人的caveChoice
        origin_cave_choice = player_tag.getElementsByTagName("caveChoice")[0].firstChild.nodeValue
        new_cave_choice = new_player_tag.getElementsByTagName("caveChoice")[0].firstChild.nodeValue
        player_tag.getElementsByTagName("caveChoice")[0].firstChild.nodeValue = new_cave_choice
        new_player_tag.getElementsByTagName("caveChoice")[0].firstChild.nodeValue = origin_cave_choice
        # 将新主持人的tag返回，用于保存SaveGameInfo
        returnTag = new_player_tag.cloneNode(True)
        returnTag.tagName = 'Farmer'
        # returnTag.setAttributes({
        #     "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        #     "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
        # })
        returnTag.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        returnTag.setAttribute("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
        return returnTag

    def save(self, file_path=None):
        if file_path is None:
            file_path = self.file_path
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.dom.toxml(encoding="utf-8"))

    def to_xml(self):
        return self.dom.toxml(encoding="utf-8")



