from datetime import datetime
from prettytable import PrettyTable as pt

valid = {
    '0':(['INDI','FAM'],'HEAD','TRLR','NOTE'),
    '1':('NAME','SEX','BIRT','DEAT','FAMC','FAMS','MARR','HUSB','WIFE','CHIL','DIV'),
    '2':('DATE'),
} # dictionary stores valid tags


def age_cal(birthday): # calculate individual's age
    birthdate = datetime.strptime(birthday, '%d%b%Y')
    current = datetime.today()
    return current.year - birthdate.year - ((current.month, current.day) < (birthdate.month, birthdate.day))

def parse_file(path,encode = 'utf-8'):
    """read the file from the path, based on level and tag scratch the information line by line and store in the dictionary,
       print the summary of individuals and families
    """
    with open(path,'r',encoding=encode) as ged_file:
        isValid = 'N'
        IsIND = True
        indi = {}
        fam = {}
        currentDate = ''
        currentInd = ''
        currentFam = ''
        for line in ged_file:    
            word_list = line.strip().split()
            arguments = ''.join(word_list[2:])
            tag = 'NA'
            level = 'NA'

            # verify each line's validity
            if len(word_list) == 1:
                level = word_list[0]
            elif len(word_list) > 1:
                level = word_list[0]
                tag = word_list[1]

            if len(word_list) == 3 and word_list[0] == '0' and word_list[2] in ('INDI', 'FAM'):
                isValid = 'Y'
                tag = word_list[2]
            elif len(word_list) > 1 and level in valid and tag in valid[level]:
                isValid = 'Y'
            
            if isValid == 'Y':   # only read the valid line
                if level== '0' and tag == 'INDI':
                    currentInd = word_list[1]
                    IsIND = True
                    indi[currentInd] = {'id':word_list[1]}   # key for each individual

                if IsIND:    # information about the individual if true
                    if level == '1' and tag == 'NAME':
                        indi[currentInd]['name'] = arguments   # store name
                    if level == '1' and tag == 'BIRT' or tag == 'DEAT':
                        currentDate = tag 
                    if level == '2' and currentDate != '' and tag == 'DATE':   # store birth date or death date
                        indi[currentInd][currentDate] = arguments   

                    if level == '1' and tag == 'SEX':   # store sex
                        indi[currentInd]['sex'] = arguments   
                    if level == '1' and tag in ('FAMC','FAMS'):   # store family information: child in the family, or spouse in the family
                        if tag in indi[currentInd]:
                            indi[currentInd][tag].add(arguments)
                        else:
                            indi[currentInd][tag] = {arguments}  
   
                if level=='0' and tag == 'FAM':   #  change to information about the family, info for individual is over at here
                    IsIND = False
                    currentFam = word_list[1]
                    fam[currentFam] = {'fam':currentFam}   # store key for the family dictionary
                    
                if IsIND == False:
                    if level == '1' and word_list[1] == 'MARR' or word_list[1] == 'DIV':   # store marriage date and divorce date
                        currentDate = tag
                    if level == '2' and tag == 'DATE':
                        fam[currentFam][currentDate] =arguments
                    if level == '1' and tag in ('HUSB','WIFE'):   # store role in the family, husband or wife
                        fam[currentFam][tag] = arguments
                    if level == '1' and tag == 'CHIL':   # store children in the family
                        if tag in fam[currentFam]:
                            fam[currentFam][tag].add(arguments)
                        else:
                            fam[currentFam][tag] = {arguments}

        # define the schema to print individual table
        indiTable = pt(["ID", "NAME", "Gender", "BDay", "Age", "Death", "Child", "Spouse"])
        for key in indi.keys():
            birth = datetime.strptime(indi[key]['BIRT'],'%d%b%Y')  # print birth date
            birth_str = birth.strftime('%Y-%m-%d')
            
            if 'DEAT' in indi[key]:   # print death date
                death = datetime.strptime(indi[key]['DEAT'],'%d%b%Y')
                death_str = death.strftime('%Y-%m-%d')
            else:
                death_str ='NA'

            if 'FAMC' in indi[key]:
                child = indi[key]['FAMC']
            else:
                child = None
            
            if 'FAMS' in indi[key]:
                spouse = indi[key]['FAMS']
            else:
                spouse = 'NA'

            age = age_cal(indi[key]['BIRT'])
            indiTable.add_row([indi[key]['id'],indi[key]['name'],indi[key]['sex'], birth_str, age, death_str, child, spouse])

        # define the schema to print family table
        famTable =pt(['ID','Married','Divorced','Husband ID','Husband Name','Wife ID','Wife name','Children'])
        for key in fam.keys():
            if 'DIV' in fam[key]:   # print divorce date
                div = datetime.strptime(fam[key]['DIV'],'%d%b%Y')
                div_str = div.strftime('%Y-%m-%d')

            else: 
                div_str = "NA"

            if "HUSB" in fam[key]:   # print husband ID and his name
                hubID = fam[key]['HUSB']
                hubName = indi[hubID]['name']
            else:
                hubID = "NA"
                hubName = "NA"

            if "WIFE" in fam[key]:   # print wife ID and her name
                wifeID = fam[key]['WIFE']
                wifeName = indi[wifeID]['name']
            else:
                wifeID = "NA"
                wifeName = "NA"

            if 'CHIL' in fam[key] :   # print set for children in the family
                chil = fam[key]['CHIL']
            else:
                chil = "NA"

            if 'MARR' in fam[key]:   # print marriage date
                marr = datetime.strptime(fam[key]['MARR'],'%d%b%Y')
                marr_str = marr.strftime('%Y-%m-%d')
            else:
                marr_str = "NA"

            famTable.add_row([key, marr_str, div_str, hubID, hubName, wifeID, wifeName, chil])
        
        print(indiTable)
        print(famTable)

    return {'fam':fam, 'indi':indi}


r = parse_file('Anirudh.ged')  