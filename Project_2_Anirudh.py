'''Code by: Anirudh Bezzam'''

def ged_parser(path):
    """Radd the contains of file"""
    try:
        gp = open(path, 'r')
    except FileNotFoundError:   # exception handling
        raise FileNotFoundError("File not found : ", path)
    else:
        with gp:                # file_opener, confused as to where to use the UTF encoding
            for line_num, line in enumerate(gp):
                fields = line.strip().split()
                if len(fields) >= 3:
                    fields = line.strip().split(" ",2)
                elif len(fields) < 1:
                    raise ValueError("Excepted number of fields is not present in row.")
                else:
                    fields = line.strip().split()
                    fields.append("")
                yield fields

def main():
    for level, tag, case in ged_parser(path):   # splitter into level tag case: invalid or valid
        print('-->', level, tag, case)
        result = list()

        '''Aim is to store important_tags as a dictionary so as to easily reference it'''
        
        important_tags = {'NAME': '1', 'SEX': '1','MARR': '1',
                      'BIRT': '1', 'DEAT': '1', 'FAMC': '1', 'FAMS': '1',
                      'HUSB': '1', 'WIFE': '1', 'CHIL': '1',
                      'DIV': '1', 'DATE': '2', 'HEAD': '0', 'TRLR': '0', 'NOTE': '0'}
        
        special_important_tags = {'INDI': '0','FAM': '0'}

        valid_tag_level = False
        if case in ['INDI', 'FAM']:
            special_tags = True
            for current_tag, current_level in special_important_tags.items():
                if level == current_level and case == current_tag:
                    valid_tag_level = True
                    break
        else:
            special_tags = False
            for current_tag, current_level in important_tags.items():
                if level == current_level and tag == current_tag:
                    valid_tag_level = True
                    break

        if valid_tag_level and special_tags:
            result.append(level)
            result.append(case)
            result.append("Y")
            result.append(tag)
        
        elif not valid_tag_level and not special_tags:
            result.append(level)
            result.append(tag)
            result.append("N")
            result.append(case)
        
        elif valid_tag_level and not special_tags:
            result.append(level)
            result.append(tag)
            result.append("Y")
            result.append(case)
        
        else:
            result.append(level)
            result.append(case)
            result.append("N")
            result.append(tag)
        print('<--', "|".join(result))


if __name__ == '__main__':
    path = 'Anirudh.ged'
    main()