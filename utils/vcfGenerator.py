import vobject
import zipfile
import io
def generateVcard(row, headers, vCards):
    vcard = vobject.vCard()

    fn = row.get(headers.get("First Name","Not Found"),"")+row.get(headers.get("Last Name","Not Found"),"")
    if fn:
        vcard.add("fn").value = fn

    vcard.add("n").value = vobject.vcard.Name(
        family=row.get(headers.get("Last Name","Not Found"),""),
        given=row.get(headers.get("First Name","Not Found"),""),
        additional=row.get(headers.get("Middle Name","Not Found"),""),
        suffix=row.get(headers.get("Suffix","Not Found"),""),
        prefix=row.get(headers.get("Prefix","Not Found"),"")
    )

    phones = (row.get(headers.get("Phone Number","Not Found"),""))
    if phones:
        for phone in (row.get(headers.get("Phone Number","Not Found"),"")).split(","):
            telephone = vcard.add("tel")
            telephone.type_param = ["HOME"]
            telephone.value = phone
    
    vcard.add('version').value = '4.0'
    vCards.append(vcard)

def generateVcf(df, headers,split):
    vCards=[]
    df.apply(lambda row: generateVcard(row,headers,vCards),axis=1)
    if not split:
        vCards = [vCard.serialize() for vCard in vCards]
        vcardString = "\n".join(vCards)
        return vcardString
    else:
        zipMemoryFile = io.BytesIO()
        with zipfile.ZipFile(zipMemoryFile,"w") as zipFile:
            for vCard in vCards:
                textFile = io.StringIO(vCard.serialize())
                zipFile.writestr(f"{vCard.fn.value} contact.vcf",textFile.getvalue())

        zipMemoryFile.seek(0)
        return zipMemoryFile.getvalue()


