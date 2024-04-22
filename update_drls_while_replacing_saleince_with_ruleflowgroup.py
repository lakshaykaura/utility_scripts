import os
import re
import logging

# Setting up logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def process_file(filepath, dir_name):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

        # Removing // agenda-group "level<something>"
        agenda_group_pattern = re.compile(r'//\s*agenda-group\s*"level\d+"\s*')
        content = agenda_group_pattern.sub("", content)

        # This pattern ensures that the 'when' keyword is matched only when it's not a part of the rule name.
        rule_pattern = re.compile(r'(rule\s*"([^"]*?)")([^{}]*?)(when)', re.DOTALL)
        salience_pattern = re.compile(r"salience\s*[-]?\d+")
        ruleflow_group_pattern = re.compile(r'ruleflow-group\s*".*?"')

        # Extracting indentation before 'when' can be tricky due to potential multiple 'when' keywords in the rule names or condition.
        # It's done in the replacement logic to make sure it's applied to the correct 'when' keyword.

        def replacement_logic(match):
            rule_decl = match.group(1)
            rule_name = match.group(
                2
            )  # Extracting rule name to ensure 'when' in rule names doesn't interfere.
            between_decl_when = match.group(3)
            when_word = match.group(4)

            # Making sure the 'when' keyword from rule names doesn't interfere with our indentation logic.
            # We find the last 'when' keyword, assuming it's related to the rule condition.
            indentation_match = re.search(
                r"(\s*)when(?![^\"]*\"[^\"]*\")", between_decl_when[::-1]
            )
            indentation = indentation_match.group(1)[::-1] if indentation_match else ""

            if (
                "ruleflow-group" not in between_decl_when
                and "salience" not in between_decl_when
            ):
                # Removing any extra newline characters from between_decl_when and then adding our ruleflow-group line.
                cleaned_between = between_decl_when.strip("\n ")
                return f'{rule_decl}{cleaned_between}\n{indentation}ruleflow-group "RuleflowGroup{dir_name}"\n{indentation}{when_word}'
            else:
                return match.group(0)

        updated_content = rule_pattern.sub(replacement_logic, content)

        # Replace existing ruleflow-group or salience, if any.
        updated_content = ruleflow_group_pattern.sub(
            f'ruleflow-group "RuleflowGroup{dir_name}"', updated_content
        )
        updated_content = salience_pattern.sub(
            f'ruleflow-group "RuleflowGroup{dir_name}"', updated_content
        )

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(updated_content)


def process_folder(path):
    for foldername in os.listdir(path):
        subfolder_path = os.path.join(path, foldername)
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".drl"):
                    filepath = os.path.join(subfolder_path, filename)
                    process_file(filepath, foldername)
            logging.info(f"Finished processing sub-directory: {foldername}")


# Taking the main directory as input from user
main_directory = input("Enter the path to the main directory: ")

# Check if directory exists before processing
if os.path.exists(main_directory) and os.path.isdir(main_directory):
    process_folder(main_directory)
    logging.info("Processing completed!")
else:
    logging.error(
        f"Directory '{main_directory}' does not exist. Please provide a valid directory path."
    )
