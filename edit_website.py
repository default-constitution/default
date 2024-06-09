import xml.etree.ElementTree as ET

class WebsiteEditor:
    def __init__(self, xml_file):
        # Initialize the WebsiteEditor with the given XML file
        self.xml_file = xml_file
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
        self.changes_made = False

    # Add a new group section with the given title
    def add_group_section(self, group_title):
        group_section = ET.SubElement(self.root.find('groupSections'), 'groupSection')
        title = ET.SubElement(group_section, 'title')
        title.text = group_title
        ET.SubElement(group_section, 'contentSections')
        self.changes_made = True

    # Add a new content section to a specified group section
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

    # Edit an existing content section within a specified group section
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

    # Move a content section from one group section to another
    def move_content_section(self, old_group_title, new_group_title, section_title):
        for content_section in self.root.findall(".//groupSection[title='" + old_group_title + "']//contentSection[title='" + section_title + "']"):
            new_group_section = self.root.find(".//groupSection[title='" + new_group_title + "']")
            if new_group_section is not None:
                content_sections = new_group_section.find('contentSections')
                content_sections.append(content_section)
                old_group_section = self.root.find(".//groupSection[title='" + old_group_title + "']")
                old_group_section.find('contentSections').remove(content_section)
                self.changes_made = True

    # Delete a group section with the given title
    def delete_group_section(self, group_title):
        for group_section in self.root.findall(".//groupSection[title='" + group_title + "']"):
            self.root.find('groupSections').remove(group_section)
            self.changes_made = True

    # Delete a content section within a specified group section
    def delete_content_section(self, group_title, section_title):
        for content_section in self.root.findall(".//groupSection[title='" + group_title + "']//contentSection[title='" + section_title + "']"):
            group_section = self.root.find(".//groupSection[title='" + group_title + "']")
            group_section.find('contentSections').remove(content_section)
            self.changes_made = True

    # Move a group section above or below another group section
    def move_group_section(self, group_title, position_title, above=True):
        group_section = self.root.find(".//groupSection[title='" + group_title + "']")
        position_section = self.root.find(".//groupSection[title='" + position_title + "']")
        parent = self.root.find('groupSections')
        parent.remove(group_section)
        index = parent.getchildren().index(position_section)
        if above:
            parent.insert(index, group_section)
        else:
            parent.insert(index + 1, group_section)
        self.changes_made = True

    # Move a content section above or below another content section within a group section
    def move_content_section_within_group(self, group_title, section_title, position_title, above=True):
        group_section = self.root.find(".//groupSection[title='" + group_title + "']")
        content_section = group_section.find(".//contentSection[title='" + section_title + "']")
        position_section = group_section.find(".//contentSection[title='" + position_title + "']")
        parent = group_section.find('contentSections')
        parent.remove(content_section)
        index = parent.getchildren().index(position_section)
        if above:
            parent.insert(index, content_section)
        else:
            parent.insert(index + 1, content_section)
        self.changes_made = True

    # Save changes made to the XML file
    def save_changes(self):
        xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
        stylesheet = '<?xml-stylesheet type="text/xsl" href="style.xsl"?>\n'
        xml_string = ET.tostring(self.root, encoding='unicode')
        with open(self.xml_file, 'w') as file:
            file.write(xml_declaration)
            file.write(stylesheet)
            file.write(xml_string)
        self.changes_made = False

    # Discard changes and reload the XML file
    def discard_changes(self):
        self.tree = ET.parse(self.xml_file)
        self.root = self.tree.getroot()
        self.changes_made = False

    # Display available methods and their descriptions
    def help(self):
        return """
        WebsiteEditor Methods:
        1. add_group_section(group_title) - Adds a new group section with the given title.
        2. add_content_section(group_title, url, title, description, image=None, hashtags=None) - Adds a new content section to the specified group section.
        3. edit_content_section(group_title, old_title, new_url=None, new_title=None, new_description=None, new_image=None, new_hashtags=None) - Edits an existing content section in the specified group section.
        4. move_content_section(old_group_title, new_group_title, section_title) - Moves a content section from one group section to another.
        5. delete_group_section(group_title) - Deletes a group section with the given title.
        6. delete_content_section(group_title, section_title) - Deletes a content section within the specified group section.
        7. move_group_section(group_title, position_title, above=True) - Moves a group section above or below another group section.
        8. move_content_section_within_group(group_title, section_title, position_title, above=True) - Moves a content section above or below another content section within a group section.
        9. save_changes() - Saves the changes made to the XML file.
        10. discard_changes() - Discards the changes made and reloads the XML file.
        """

def main():
    editor = WebsiteEditor('index.xml')

    while True:
        print("\nWebsite Editor Options:")
        print("1. Add a new group section")
        print("2. Add a new content section")
        print("3. Edit an existing content section")
        print("4. Move a content section to another group")
        print("5. Delete a group section")
        print("6. Delete a content section")
        print("7. Move a group section")
        print("8. Move a content section within a group")
        print("9. Save changes")
        print("10. Discard changes")
        print("11. Exit")
        
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
            group_title = input("Enter the title of the group section to delete: ")
            editor.delete_group_section(group_title)
            print(f"Deleted group section '{group_title}'")

        elif choice == '6':
            group_title = input("Enter the group title of the content section to delete: ")
            section_title = input("Enter the title of the content section to delete: ")
            editor.delete_content_section(group_title, section_title)
            print(f"Deleted content section '{section_title}' in group '{group_title}'")

        elif choice == '7':
            group_title = input("Enter the title of the group section to move: ")
            position_title = input("Enter the title of the group section to move above/below: ")
            above = input("Move above? (yes/no): ").lower() == 'yes'
            editor.move_group_section(group_title, position_title, above)
            print(f"Moved group section '{group_title}' {'above' if above else 'below'} '{position_title}'")

        elif choice == '8':
            group_title = input("Enter the title of the group containing the content sections: ")
            section_title = input("Enter the title of the content section to move: ")
            position_title = input("Enter the title of the content section to move above/below: ")
            above = input("Move above? (yes/no): ").lower() == 'yes'
            editor.move_content_section_within_group(group_title, section_title, position_title, above)
            print(f"Moved content section '{section_title}' {'above' if above else 'below'} '{position_title}' in group '{group_title}'")

        elif choice == '9':
            editor.save_changes()
            print("Changes saved.")

        elif choice == '10':
            editor.discard_changes()
            print("Changes discarded.")

        elif choice == '11':
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
