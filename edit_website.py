import xml.etree.ElementTree as ET

class WebsiteEditor:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
        self.changes_made = False

    def add_group_section(self, group_title):
        group_section = ET.SubElement(self.root.find('groupSections'), 'groupSection')
        title = ET.SubElement(group_section, 'title')
        title.text = group_title
        ET.SubElement(group_section, 'contentSections')
        self.changes_made = True

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
            self.changes_made = True

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
            self.changes_made = True

    def move_content_section(self, old_group_title, new_group_title, section_title):
        for content_section in self.root.findall(".//groupSection[title='" + old_group_title + "']//contentSection[title='" + section_title + "']"):
            new_group_section = self.root.find(".//groupSection[title='" + new_group_title + "']")
            if new_group_section is not None:
                content_sections = new_group_section.find('contentSections')
                content_sections.append(content_section)
                old_group_section = self.root.find(".//groupSection[title='" + old_group_title + "']")
                old_group_section.find('contentSections').remove(content_section)
                self.changes_made = True

    def save_changes(self):
        self.tree.write(self.xml_file)
        self.changes_made = False

    def discard_changes(self):
        self.tree = ET.parse(self.xml_file)
        self.root = self.tree.getroot()
        self.changes_made = False

    def help(self):
        return """
        WebsiteEditor Methods:
        1. add_group_section(group_title) - Adds a new group section with the given title.
        2. add_content_section(group_title, url, title, description, image=None, hashtags=None) - Adds a new content section to the specified group section.
        3. edit_content_section(group_title, old_title, new_url=None, new_title=None, new_description=None, new_image=None, new_hashtags=None) - Edits an existing content section in the specified group section.
        4. move_content_section(old_group_title, new_group_title, section_title) - Moves a content section from one group section to another.
        5. save_changes() - Saves the changes made to the XML file.
        6. discard_changes() - Discards the changes made and reloads the XML file.
        """

def main():
    editor = WebsiteEditor('website.xml')

    while True:
        print("\nWebsite Editor Options:")
        print("1. Add a new group section")
        print("2. Add a new content section")
        print("3. Edit an existing content section")
        print("4. Move a content section to another group")
        print("5. Save changes")
        print("6. Discard changes")
        print("7. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            group_title = input("Enter the title of the new group section: ")
            editor.add_group_section(group_title)
            print(f"Added new group section '{group_title}'")

        elif choice == '2':
            group_title = input("Enter the group title where the new content section will be added: ")
            url = input("Enter the URL: ")
            title = input("Enter the title: ")
            description = input("Enter the description: ")
            image = input("Enter the image URL (or leave blank): ")
            hashtags = input("Enter the hashtags (or leave blank): ")
            editor.add_content_section(group_title, url, title, description, image or None, hashtags or None)
            print(f"Added new content section to group '{group_title}'")

        elif choice == '3':
            group_title = input("Enter the group title of the content section to edit: ")
            old_title = input("Enter the current title of the content section: ")
            new_url = input("Enter the new URL (or leave blank to keep current): ")
            new_title = input("Enter the new title (or leave blank to keep current): ")
            new_description = input("Enter the new description (or leave blank to keep current): ")
            new_image = input("Enter the new image URL (or leave blank to keep current): ")
            new_hashtags = input("Enter the new hashtags (or leave blank to keep current): ")
            editor.edit_content_section(group_title, old_title, new_url or None, new_title or None, new_description or None, new_image or None, new_hashtags or None)
            print(f"Edited content section '{old_title}' in group '{group_title}'")

        elif choice == '4':
            old_group_title = input("Enter the current group title of the content section: ")
            new_group_title = input("Enter the new group title where the content section will be moved: ")
            section_title = input("Enter the title of the content section to move: ")
            editor.move_content_section(old_group_title, new_group_title, section_title)
            print(f"Moved content section '{section_title}' from '{old_group_title}' to '{new_group_title}'")

        elif choice == '5':
            editor.save_changes()
            print("Changes saved.")

        elif choice == '6':
            editor.discard_changes()
            print("Changes discarded.")

        elif choice == '7':
            if editor.changes_made:
                save = input("You have unsaved changes. Do you want to save them before exiting? (yes/no): ").lower()
                if save == 'yes':
                    editor.save_changes()
                    print("Changes saved.")
                else:
                    editor.discard_changes()
                    print("Changes discarded.")
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
