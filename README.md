# Linkedin Parsers

## Intro
A collection of parser scripts created to scrape data off LinkedIn. The main one is ```linkedin2email.py```, to be honest you don't need to use ```linkedin-parser.py``` and ```name2email-v2.py```, they are kept here for sentimental reason. And because I can.

## Background
Initially it was a two-part process:
1. Use ```linkedin-parser.py``` to parse the web log from Burp, to create a CSV
2. Use ```name2email-v2.py``` to read an Excel file to generate email formats

This is obviously laborious, it is for that reason ```linkedin2email.py``` is created to take away the extra steps.

## Process
The process works like this:
1. With traffic proxying through Burp, log in to LinkedIn on a web browser and search for the company. That should generate tonnes of requests, among them this:
```
/voyager/api/search/blended?count=40&filters=List(currentCompany-%3E{companyId}},resultType-%3EPEOPLE)&origin=OTHER&q=all&queryContext=List(spellCorrectionEnabled-%3Etrue,relatedSearchesEnabled-%3Etrue)&start=0
```
2. Send it to Burp repeater and play it a few times until we hit the value mentioned in ```totalResultCount``` param (you can get this value from the HTTP response body) and we should have a complete list of employees. Save the response locally.
3. Use ```linkedin2email.py``` for your parsing pleasure, provide it with the location of the saved file and the domain name.
4. Profit?

## Usage
For the sake of demonstration, let's imagine you are red-teaming E Corp and because of limited Internet footprint, you could not find a lot of email addresses of the target organisation from sources such as data breaches. You then decided to give LinkedIn a go. You logged in, searched for E Corp with Burp running as your proxy. You then saved the responses to a file locally. The content should look like below *(accurate as of 11 June 2020; LinkedIn does change stuff from time to time, so the accuracy of the response body might have changed after this date)*:
```
GET /voyager/api/search/blended?count=40&filters=List(currentCompany-%3E{companyId}},resultType-%3EPEOPLE)&origin=OTHER&q=all&queryContext=List(spellCorrectionEnabled-%3Etrue,relatedSearchesEnabled-%3Etrue)&start=0 HTTP/1.1
Host: www.linkedin.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: application/vnd.linkedin.normalized+json+2.1
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://www.linkedin.com/company/ecorp/
x-li-lang: en_US
{...truncated for brevity...}


HTTP/1.1 200 OK
Cache-Control: no-cache, no-store
Pragma: no-cache
Content-Length: 96702
Content-Type: application/vnd.linkedin.normalized+json+2.1; charset=UTF-8
Expires: Thu, 01 Jan 1970 00:00:00 GMT
{...truncated for brevity...}

{"data":{"metadata":{"totalResultDisplayText":{"text":"290 results","$type":"com.linkedin.voyager.common.TextViewModel"},"searchId":"069ce6a3-765a-427a-9337-6f8cb06490dc","totalResultCount":290,"origin":"OTHER","numVisibleResults":40,"$type":"com.linkedin.voyager.search.BlendedSearchMetadata"},"entityUrn":"urn:li:collectionResponse:iWS49EODL9ISfkfOCcNZY2yikfmaWBLAA+PsGKDLiMw=","elements":[{"extendedElements":[{"searchTieIn":"FREE_UPSELL","type":"SEARCH_TIE_IN","$type":"com.linkedin.voyager.search.ExtendedSearchHit"}],"elements":[],"type":"SEARCH_FEATURES","$type":"com.linkedin.voyager.search.BlendedSearchCluster"},{"extendedElements":[],"elements":[{"memberDistance":{"value":"DISTANCE_3","$type":"com.linkedin.voyager.common.MemberDistance"},"image":{"attributes":[{"sourceType":"PROFILE_PICTURE","*miniProfile":"urn:li:fs_miniProfile:ACoAAAFFtjkBJFXV-YqyxPfQV-1SbQIVjXmnJDo","$type":"com.linkedin.voyager.common.ImageAttribute"}],"accessibilityTextAttributes":[],"$type":"com.linkedin.voyager.common.ImageViewModel"},"targetUrn":"urn:li:fs_miniProfile:ACoAAAFFtjkBJFXV-YqyxPfQV-1SbQIVjXmnJDo","socialProofImagePile":[],"trackingUrn":"urn:li:member:21345849","navigationUrl":"https://www.linkedin.com/in/kumar-asaka-b091947","title":{"textDirection":"USER_LOCALE","text":"Kumar Asaka","$type":"com.linkedin.voyager.common.TextViewModel"},"type":"PROFILE","$type":"com.linkedin.voyager.search.SearchHitV2","headless":false,"socialProofText":"0 shared connections","secondaryTitle":{"textDirection":"USER_LOCALE","text":"3rd+","$type":"com.linkedin.voyager.common.TextViewModel"},"*badges":"urn:li:fs_memberBadges:ACoAAAFFtjkBJFXV-YqyxPfQV-1SbQIVjXmnJDo","publicIdentifier":"kumar-asaka-b091947","headline":{"textDirection":"USER_LOCALE","text":"Program Director at E Corp","$type":"com.linkedin.voyager.common.TextViewModel"},"nameMatch":false,"subline":{"textDirection":"USER_LOCALE","text":"Tonbridge, United Kingdom","$type":"com.linkedin.voyager.common.TextViewModel"},"trackingId":"wSKPl/GARVmSoNPEnhxBeQ=="}
```

Now you can just point the script to the file location, plus providing the domain name so that it will be appended automagically for you.
```
PS C:\LinkedIn-parser> python linkedin2email.py -i "./linkedin-ecorp-001-320.log" -d ecorp.com
[*] CSV file saved at:        C:\LinkedIn-parser\names_positions.csv
[*] Email lists saved under:  C:\LinkedIn-parser\ecorp.com\*
```

You should now have the CSV file and email address lists ready:
```
PS C:\LinkedIn-parser> ls


    Directory: C:\LinkedIn-parser


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----       11/06/2020     21:35                ecorp.com
-a----       11/06/2020     17:55         638244 linkedin-ecorp-001-320.log
-a----       11/06/2020     21:37           5559 linkedin2email.py
-a----       11/06/2020     21:36           5206 names_positions.csv
```

The content of the CSV file should look like this, giving you a nice understanding of who holds what position within the target organisation:
```
Name,Job Description
Kumar Asaka,Program Director at E Corp
Khaled Hadley,Vice President for Innovation at E Corp
Yamin Nishikov,Commercial sales
Salman Alexander,Program/Project Controller
Norah AlMugreen,Governance and Compliance Senior Manager at E Corp
Camila Roberta,Business Analytics Senior Manager at E Corp
Omar AlAbdullah,Talent Management & Acquisition Sr. Officer at E Corp
Leroy Matar,Cybersecurity | Information Security | Network Security
Khaled Cabellos,Director Information Security
Ahmed Mazlan ,Information Security Architect at E Corp
Nicolas Sadiq,Teradata Data Consultant| Teradata Certified | ETL/DWH/BI | ISTQB® CTFL
Maha Djokovic,Chief Human Resources Officer
Nora AlAhmad,Talent Management and Acquisition Manager at E Corp
Quan Murrayfield,IT Consultant at E Corp
Hafiz Al Mukhriz,Managing Director at E Corp
```

Peeking inside the newly created directory/folder, email addresses in seven different formats were generated:
```
PS C:\LinkedIn-parser> ls .\ecorp.com\


    Directory: C:\LinkedIn-parser\ecorp.com


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----       11/06/2020     21:36           2381 first.last.txt
-a----       11/06/2020     21:36           1636 first.txt
-a----       11/06/2020     21:36           1729 firstl.txt
-a----       11/06/2020     21:36           2288 firstlast.txt
-a----       11/06/2020     21:36           2381 first_last.txt
-a----       11/06/2020     21:36           1859 flast.txt
-a----       11/06/2020     21:36           1859 lastf.txt
```

The output of these files are displayed in the following section.

### {first_initial}{last}@{domain}
```
kasaka@ecorp.com
khadley@ecorp.com
ynishikov@ecorp.com
salexander@ecorp.com
nalmugreen@ecorp.com
croberta@ecorp.com
oalabdullah@ecorp.com
lmatar@ecorp.com
kcabellos@ecorp.com
amazlan@ecorp.com
nsadiq@ecorp.com
mdjokovic@ecorp.com
nalahmad@ecorp.com
qmurrayfield@ecorp.com
halmukhriz@ecorp.com
```
### {first}{last}@{domain}
```
kumarasaka@ecorp.com
khaledhadley@ecorp.com
yaminnishikov@ecorp.com
salmanalexander@ecorp.com
norahalmugreen@ecorp.com
camilaroberta@ecorp.com
omaralabdullah@ecorp.com
leroymatar@ecorp.com
khaledcabellos@ecorp.com
ahmedmazlan@ecorp.com
nicolassadiq@ecorp.com
mahadjokovic@ecorp.com
noraalahmad@ecorp.com
quanmurrayfield@ecorp.com
hafizalmukhriz@ecorp.com
```
### {first}.{last}@{domain}
```
kumar.asaka@ecorp.com
khaled.hadley@ecorp.com
yamin.nishikov@ecorp.com
salman.alexander@ecorp.com
norah.almugreen@ecorp.com
camila.roberta@ecorp.com
omar.alabdullah@ecorp.com
leroy.matar@ecorp.com
khaled.cabellos@ecorp.com
ahmed.mazlan@ecorp.com
nicolas.sadiq@ecorp.com
maha.djokovic@ecorp.com
nora.alahmad@ecorp.com
quan.murrayfield@ecorp.com
hafiz.almukhriz@ecorp.com
```
### {first}_{last}@{domain}
```
kumar_asaka@ecorp.com
khaled_hadley@ecorp.com
yamin_nishikov@ecorp.com
salman_alexander@ecorp.com
norah_almugreen@ecorp.com
camila_roberta@ecorp.com
omar_alabdullah@ecorp.com
leroy_matar@ecorp.com
khaled_cabellos@ecorp.com
ahmed_mazlan@ecorp.com
nicolas_sadiq@ecorp.com
maha_djokovic@ecorp.com
nora_alahmad@ecorp.com
quan_murrayfield@ecorp.com
hafiz_almukhriz@ecorp.com
```
### {first}{last_initial}@{domain}
```
kumara@ecorp.com
khaledh@ecorp.com
yaminn@ecorp.com
salmana@ecorp.com
noraha@ecorp.com
camilar@ecorp.com
omara@ecorp.com
leroym@ecorp.com
khaledc@ecorp.com
ahmedm@ecorp.com
nicolass@ecorp.com
mahad@ecorp.com
noraa@ecorp.com
quanm@ecorp.com
hafiza@ecorp.com
```
### {first}@{domain}
```
kumar@ecorp.com
khaled@ecorp.com
yamin@ecorp.com
salman@ecorp.com
norah@ecorp.com
camila@ecorp.com
omar@ecorp.com
leroy@ecorp.com
khaled@ecorp.com
ahmed@ecorp.com
nicolas@ecorp.com
maha@ecorp.com
nora@ecorp.com
quan@ecorp.com
hafiz@ecorp.com
```
### {last}{first_initial}@{domain}
```
asakak@ecorp.com
hadleyk@ecorp.com
nishikovy@ecorp.com
alexanders@ecorp.com
almugreenn@ecorp.com
robertac@ecorp.com
alabdullaho@ecorp.com
matarl@ecorp.com
cabellosk@ecorp.com
mazlana@ecorp.com
sadiqn@ecorp.com
djokovicm@ecorp.com
alahmadn@ecorp.com
murrayfieldq@ecorp.com
almukhrizh@ecorp.com
```
