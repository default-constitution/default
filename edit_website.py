import xml.etree.ElementTree as ET

class WebsiteEditor:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()

    def add_group_section(self, group_title):
        group_section = ET.SubElement(self.root.find('groupSections'), 'groupSection')
        title = ET.SubElement(group_section, 'title')
        title.text = group_title
        ET.SubElement(group_section, 'contentSections')
        self.tree.write(self.xml_file)

    def add_content_section(self, group_title, url, title, description, image=None, hashtags=None):
        for group_section in self.root.findall(".//groupSection[title='" + group_title + "']"):
            content_section = ET.SubElement(group_section.find('contentSections'), 'contentSection')
            ET.SubElement(content_section, 'url').text = url
            ET.SubElement(content_section, 'title').text = title
            ET.SubElement(content_section, 'description').text = description
            if image:
                ET.SubElement(content_section, 'image').text = image
            if hashtags:
                ET.SubElement(content_section, 'hashtags').text = hashtags
            self.tree.write(self.xml_file)

    def edit_content_section(self, group_title, old_title, new_url=None, new_title=None, new_description=None, new_image=None, new_hashtags=None):
        for content_section in self.root.findall(".//groupSection[title='" + group_title + "']//contentSection[title='" + old_title + "']"):
            if new_url:
                content_section.find('url').text = new_url
            if new_title:
                content_section.find('title').text = new_title
            if new_description:
                content_section.find('description').text = new_description
            if new_image:
                content_section.find('image').text = new_image
            if new_hashtags:
                content_section.find('hashtags').text = new_hashtags
            self.tree.write(self.xml_file)

    def move_content_section(self, old_group_title, new_group_title, section_title):
        for content_section in self.root.findall(".//groupSection[title='" + old_group_title + "']//contentSection[title='" + section_title + "']"):
            new_group_section = self.root.find(".//groupSection[title='" + new_group_title + "']")
            if new_group_section is not None:
                content_sections = new_group_section.find('contentSections')
                content_sections.append(content_section)
                old_group_section = self.root.find(".//groupSection[title='" + old_group_title + "']")
                old_group_section.find('contentSections').remove(content_section)
                self.tree.write(self.xml_file)

    def help(self):
        return """
        WebsiteEditor Methods:
        1. add_group_section(group_title) - Adds a new group section with the given title.
        2. add_content_section(group_title, url, title, description, image=None, hashtags=None) - Adds a new content section to the specified group section.
        3. edit_content_section(group_title, old_title, new_url=None, new_title=None, new_description=None, new_image=None, new_hashtags=None) - Edits an existing content section in the specified group section.
        4. move_content_section(old_group_title, new_group_title, section_title) - Moves a content section from one group section to another.
        """

# Usage Example
if __name__ == "__main__":
    editor = WebsiteEditor('index.xml')
    editor.add_group_section('New Group')
    editor.add_content_section('New Group', 'http://example.com', 'Example Title', 'Example description', 'http://example.com/image.jpg', '#example #test')
    print(editor.help())
