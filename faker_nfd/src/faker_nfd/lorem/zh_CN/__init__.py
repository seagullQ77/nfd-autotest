from faker.providers.lorem import Provider as FakerProvider

class Provider(FakerProvider):
    crops_list = {'水稻', '豆类', '薯类', '青稞', '蚕豆', '小麦', '油籽', '蔓青', '大芥', '胡麻', '大麻',
                  '向日葵', '萝卜', '白菜', '芹菜', '韭菜', '蒜', '葱', '胡萝卜', '菜瓜', '莲花菜', '菊芋',
                  '刀豆', '芫荽', '莴笋', '黄花', '辣椒', '黄瓜', '西红柿', '梨', '苹果', '桃', '杏', '核桃',
                  '李子', '樱桃', '草莓', '林檎', '酸梨', '野杏', '毛桃', '苞瑙', '山樱桃', '沙棘', '草莓',
                  '玉米', '绿肥', '紫云英', '烟草', '咖啡', '人参', '当归', '金银花'}

    def crops(cls):
        """
        Generate a random crops
        :example '草莓'
        """
        return cls.random_element(cls.crops_list)