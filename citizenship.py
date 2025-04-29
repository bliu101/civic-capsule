from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import undetected_chromedriver as uc
import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "rocketchat")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["citizenshipday"]

# The string you want to insert
description = """
Boston Citizenship Day is New England’s largest one-day citizenship application workshop, 
where hundreds of permanent residents receive free legal assistance to begin their journey toward U.S. citizenship.
Hosted annually by Project Citizenship in collaboration with the City of Boston, this event helps eligible residents 
apply for citizenship and fee waivers with support from attorneys and trained volunteers.

What Happens on Citizenship Day?
Boston Citizenship Day is a free, one-day event that helps lawful permanent residents begin their journey toward U.S. citizenship. Volunteer attorneys, law students, and community members come together to offer free legal guidance and help with fee waivers for low-income applicants.
Since Boston “Cit Day” began in 2014, we’ve helped over 3,000 participants, from more than 100 countries, complete applications and over 1,800 fee waivers. In 2025, we served more than 300 aspiring citizens in just one day.

Event Details
Date: April 12, 2025
Time: 10:00 AM – 3:00 PM
Location: Reggie Lewis Track and Athletic Center, 1350 Tremont Street, Boston, MA 02120
Price: Free

How to Sign Up
Step 1: Check Your Eligibility
Before signing up, we need to confirm that you’re eligible for U.S. citizenship. There are 3 different ways you can complete this step:

Call us at 617-694-5949 to complete a screening over the phone with a staff member.
Schedule an eligibility call online with one of our team members.
Comfortable using a computer or smartphone? Complete our online eligibility screening form.
Important: Due to high call volumes before Boston Citizenship Day, we strongly encourage you to book your eligibility call online or complete our online eligibility screening form and send questions via email to info@projectcitizenship.org.

Step 2: Get Scheduled for Boston Citizenship Day
If you’re eligible after the screening, we’ll reach out to you to schedule a time slot for Boston Citizenship Day.

Schedule your eligibility screening call: http://outlook.office365.com/book/ProjectCitizenship1@projectcitizenship.org/
Get screened for your eligibility online: https://procit.my.site.com/Portal/s/application-screening-form

Why Attend Boston Citizenship Day?
Free Legal Assistance:
Get help completing your citizenship application from experienced attorneys and volunteers.
Fee Waiver Assistance:
If you qualify, we will help you apply for fee waivers to cover the cost of your citizenship application fees.
Community Support:
Connect with fellow applicants, volunteers, and community organizations who may be able to offer resources, and are here to offer guidance and encouragement as you take the next step toward citizenship

What benefits come with US Citizenship?
90% of immigrants who are eligible to apply for citizenship *do not* apply for citizenship. We aim to bridge that gap to support immigrants in accessing the benefits of citizenship. United States citizenship provides many privileges and benefits. 

Below are 10 unique benefits of citizenship:

1.The Right to Vote: Direct participation in democratic elections is one of the most important privileges that this country offers its citizens. Only U.S. citizens have the right to vote in federal elections and to be candidates in most local, state and federal elections.

2. Family Reunification: U.S. citizens can petition for overseas family members to receive Green Cards and immigrate legally to the United States. Relatives of citizens are given priority by U.S. Citizenship and Immigration Services.

3. Citizenship for Children: Children of citizens receive automatic citizenship if they are under 18 years of age and have a Green Card. In most cases, this includes children born abroad to U.S. citizens.

4. Security in the United States: Your right to remain in the United States as a U.S. citizen cannot be taken away. When you naturalize, your chances of deportation go down to ZERO.

5. Freedom of Travel: U.S. citizens can travel outside of the country for unlimited periods of time and to any country they wish, without any fear of this affecting their immigration status.

6. Additional Government Benefits: You may qualify for certain government benefits that are only available to citizens.

7. Additional Job Opportunities: The federal government is one of the biggest employers in the world and offers many job opportunities in a wide range of industries. However, the vast majority of federal jobs are available only to U.S. citizens.

8. More Student Aid: The federal government has different types of financial assistance for students, including scholarships and grants that are available exclusively for U.S. citizens.

9. International Protection: The United States protects its citizens abroad through its embassies and consulates. The U.S. government assists citizens who are victims of crimes overseas and provides aid to U.S. citizens abroad in the case of international disasters or emergencies.

10. Run for Office: Only U.S. citizens can run for Federal office and most State and local offices

Looking to Make a Difference?
Sponsorship is key to the success of Boston Citizenship Day and offers your company a unique opportunity to engage in immigration legal aid while promoting your brand to our extensive network of supporters and professionals. By partnering with us, your company allows us to provide essential legal assistance, fee waivers, and community support to individuals seeking U.S. citizenship.
Check out the 2025 Boston Citizenship Day Sponsorship Packet to learn more about how your involvement can make a lasting impact. We encourage sponsors to join and submit materials by March 20 to ensure inclusion in event promotions.

Sponsorship Packet: https://projectcitizenship.org/wp-content/uploads/2025/02/2025-Boston-Citizenship-Day-Sponsorship-Packet-1.pdf

Volunteer
with Project Citizenship
Volunteer and pro bono service increases our capacity to serve immigrants, keeps our organization cost-efficient, and involves community members in the transformative process of citizenship.

Volunteer sign up: https://procit.my.site.com/Portal/s/volunteer-registration

Who Can Volunteer?
Anyone with a passion for helping others can volunteer with Project Citizenship! No previous experience is required to become an Application Assistant. We provide all the necessary training to help you succeed in this role. If you’re a licensed attorney, you can also volunteer as a Quality Control (QC) reviewer to ensure the accuracy of citizenship applications.

What’s Needed to Volunteer?
Attend or watch mandatory training
Abide by Project Citizenship’s volunteer expectations and WISP policy

Way to Participate in a Citizenship Workshop:
Application assistance: Complete naturalization applications with pre-screened applicants. Open to non-attorneys; one-hour training required.

Quality control: Review completed applications with pre-screened applicants. Reserved for licensed attorneys and DOJ Accredited Representatives; one-hour training required.

Make a Difference in the Lives
of Thousands of Immigrants
Only 10 percent of eligible immigrants in Massachusetts apply to naturalize each year, leaving them without the rights and opportunities it provides. Your support helps Project Citizenship offer free legal assistance to break down barriers and make citizenship accessible. Our clients represent the most vulnerable and marginalized portion of eligible immigrants, as 70 percent of our clients are low-income.
The Challenge
For thousands of immigrants, the path to U.S. citizenship is filled with barriers like complex legal processes, financial hardships, and limited access to reliable assistance. Without support, many face overwhelming obstacles that prevent them from achieving their dream of becoming U.S. citizens.
Our Approach
At Project Citizenship, we believe every eligible immigrant deserves a fair chance at naturalization. We provide free, high-quality legal services to guide permanent residents through the citizenship process. Our dedicated team works tirelessly to break down barriers and empower individuals with the tools they need to succeed.
Your Impact
Your support fuels our mission, transforming lives by making citizenship a reality for those in need. Your donation helps:
✔ 1,000+ immigrants navigate the citizenship process.
✔ 850+ individuals receive financial or disability assistance.
✔ 40+ application assistance workshops held annually.
✔ 95 percent of our applicants achieve U.S. citizenship.

Donate: https://projectcitizenship.org/donate/?cmd=_s-xclick&hosted_button_id=L6X8NR76QGTUL&submit.x=109&submit.y=131
Other ways to give:
DONATE THROUGH A DONOR ADVISED FUND
Maximize your philanthropy through a DAF account.
Give now from yourDonor-Advised Fund: https://projectcitizenship.org/donate/?cmd=_s-xclick&hosted_button_id=L6X8NR76QGTUL&submit.x=109&submit.y=131#

MAKE A GIFT OF STOCK
We accept charitable donations of stock and mutual funds.
Learn More: https://projectcitizenship.org/donate/gift-of-stock/

PLANNED GIVING
This option provides a way to make a charitable gift and receive favorable tax benefits.
Learn More: https://projectcitizenship.org/donate/planned-giving/

DONATE FROM AN IRA
Lower your tax bill and help our cause at the same time.
Learn More: https://projectcitizenship.org/donate/donate-from-an-ira/

DONATE BY PHONE OR MAIL
Call 617-694-5949 to donate or use these forms to print & mail your gift.
Learn More: https://projectcitizenship.org/donate/donate-by-phone-or-mail/

GIVE THROUGH WORK
Workplace giving enables employees to support through pre-tax payroll deductions and/or employee matching.
Learn More: https://projectcitizenship.org/donate/give-through-work/

Join our Legacy Club
Learn More: https://projectcitizenship.org/wp-content/uploads/2023/12/Legacy-Club.pdf

Have Questions Regarding Your Donation?
View Our Gift Acceptance Policy: https://projectcitizenship.org/wp-content/uploads/2024/04/Project-Citizenship-Gift-Acceptance-Policy-1.docx
FAQs: https://projectcitizenship.org/donate/faq/

Project Citizenship who we are
Mission Statement
Project Citizenship seeks to increase the naturalization rate in New England, with a focus on the most vulnerable and disadvantaged populations.
What We Do
We are a nonprofit agency that provides free, high-quality legal services to permanent residents to help them become U.S. citizens. Project Citizenship offers free workshops, eligibility screening, application assistance, legal referrals, and all materials needed to apply for U.S. citizenship. In addition, Project Citizenship works collaboratively with community-based partners in New England to provide a range of support services, civics instruction, application assistance, and ESOL classes.

Why We Do What We Do
Project Citizenship is a client-centered nonprofit organization.  We firmly believe that immigrants are an integral part of a healthy U.S. society.  We focus exclusively on increasing access to U.S. citizenship because we believe that focusing our modest resources on what we do best is the most effective way to ensure the highest quality of services and the best outcome for our clients. 

Our History
Since launching in 2014, Project Citizenship has specialized in helping permanent residents in Massachusetts and beyond overcome barriers to U.S. citizenship. Each year, thousands of Massachusetts residents eligible to become citizens never apply. The need for free, professional legal services to guide people through the citizenship process is evident and the demand has grown significantly, especially after 2016.

Pro bono lawyers from elite Boston law firms, Department of Justice (DOJ) accredited staff, and AmeriCorps volunteers at Project Citizenship have represented thousands of clients from around the world. Many of our clients believed citizenship was unattainable due to factors such as a one hundred question English and Civics test, costly processing fees, or a disability. After attending our workshops held regularly in the Greater Boston area and beyond, including those in Lowell and Lawrence, as well as special events like Citizenship Day, co-sponsored by the Mayor’s Office for Immigrant Advancement, our clients quickly discover that citizenship and its associated benefits are within reach.

Though it was officially launched in 2014, Project Citizenship’s roots date back to 2011 with the support of the Fish Family Foundation which is deeply committed to serving immigrant communities. A collaboration of six community partners offering comprehensive social services for immigrants including citizenship services, the Greater Boston Citizenship Initiative, came together with the support of the Fish Family Foundation. Together, they focused on how to best increase naturalization rates throughout the state. Between 2011 and 2014, the Initiative grew both in its number of partners and geographic scope.


A strategic planning process in 2014 paved the way for a nonprofit organization focused solely on citizenship services that could also guide these organizations to offer citizenship services with best practices.  Through its evolving community partnerships, Project Citizenship gained deep insights into the wider net of existing citizenship services throughout Massachusetts. A full list of partners can be found here: https://projectcitizenship.org//about-us/partners/.

As Project Citizenship focuses 100% of its attention and resources on the urgent need of helping eligible legal permanent residents become U.S. citizens, it will continue to offer its expertise and support to community partners. Since its inception, Project Citizenship has doubled revenue from private and public foundations. Project Citizenship’s dedicated full-time staff, pro bono legal partners and expansive volunteer force of more than 5,000 trained volunteers to date in 2024 have made it possible to help over 11,700 immigrants apply for U.S. citizenship with a 95% success rate.

Project Citizenship is a DOJ recognized nonprofit organization.

Awards

2019 Pride of Boston Award to Veronica Serrato

2019 MAHA (Massachusetts Association of Hispanic Attorneys) Organization of the Year

2017 Social Innovation Forum innovator

2017 Nonprofit Partner Award from Cambodian Mutual Assistance Association

2015 Massachusetts Service and Volunteerism Award for Outstanding Corporate-Nonprofit Partnership with Goodwin Procter

2015 Recognition Award from Agencia ALPHA

Success Stories: Meet some of our amazing former clients who have successfully become U.S. citizens with the support of Project Citizenship. These are just a few stories that show the strength and determination of our clients.
David's Story: When David Left “Mister” Behind  

By Nora Jarquin, 2024 Summer Intern

 

At age 11, David moved to Boston with his father and two siblings, leaving his mother in Port-au-Prince. The stark cultural differences between Haiti and America made David’s move overwhelming. In David’s home country, one would hear ‘mister’ and ‘missus’ every day, at markets, schools, and stores. David spent the first decade of his life referring to adults as ‘mister’ and ‘missus,’ a cultural custom in Haiti. ‘The manners here are different,’ David noted about his move to the U.S.

 

Over a decade has passed since David and his mother were together, fueling David’s resolve to naturalize. “That’s one of the reasons I wanted to become a citizen,” he said hoping to start the process to bring his mom to the U.S. David began the citizenship application process with Project Citizenship per recommendation from his siblings. David described his experience with us as, “Informative, straightforward, [and] helpful.”  Project Citizenship assisted David closely in the three-year process it took to achieve U.S. citizenship. “They gave me the best ways to move forward when things did not go well,” he explained.

 

Reflecting on his new rights as a citizen, David shared, “I got tired of not being able to vote.” He expressed his relief that he could vote for a candidate that prioritizes immigrants and an accessible path to citizenship in American society. David gained “Safety, opportunity, [and a] life.”

 

The day he took the oath and became a U.S. citizen, David exhaled with relief and smiled as he sat among the 200 other citizens-to-be. “It was great to see all the people trying to make their lives better and trying to be a part of this great country.” 

 

Holding a small American flag, David felt a sense of pride. Though David’s story is just one in a country full of immigrants, it serves to remind us of the connection and unity that comes with U.S. citizenship, of the possibility and hope of the new American dream. Although David no longer says “mister” and “missus,” a piece of Haiti will soon be with him in America when he petitions for his mother to come with his newfound citizenship.  


Fritz's Story: “Welcome Home!” 

by Meredith Monnich, 2024 Summer Intern

 

“Welcome home!” An officer stamped Fritz’s passport and handed it back with a smile. Fritz, a former Project Citizenship client from Haiti, looked left to observe a snaking line for non-U.S. citizens waiting to gain re-entry into the U.S. This moment was the first time he had ever entered the right lane when coming back to the U.S. from Haiti, his home country. He felt a sense of excitement — the right lane was the one for American citizens. 

Fritz’s childhood was marked by the sticky sweetness of mangoes and the joy of playing street soccer in the rain. He grew up in Haiti and thinks back on his younger years with a smile.  

“I remember going to the beach with friends and family [and] playing marbles,” Fritz said. “[Haiti] is nice, it’s gorgeous.” His youth remained like this – bright and carefree – for a long time. When Fritz thinks back to his childhood, he remembers the perfect days spent with his family at the beach.  

At the end of the summer of 1991, however, Fritz began to feel the atmosphere shift in his home country. He recounted that by September, the sudden political turmoil in Haiti caused schools to close. At that point, most of his childhood friends were already looking for ways to move away from Haiti. 

At 17, Fritz, too, boarded the plane to the United States, forced to say a difficult goodbye to his beautiful country. And it certainly wasn’t easy at first. In high school, Fritz struggled to maintain his Haitian identity in Chicago. Speaking up was difficult for him.  

“I felt bad as a senior in high school when it was my turn to speak. My accent was heavy, although I was smart in school. I was a straight-A student, but my accent was still there.” 

Fritz recounted a story of a high school bully who laughed at him every time he read aloud in class. “He affected me for a long, long time. In my life even after high school because I was shy because of him. I was afraid to talk in public spaces.” 

However, his confidence grew with each year he spent in the United States. As most of his extended family and friends joined him in the U.S., he slowly began to feel more comfortable in his new home – without ever forgetting about his life back in Haiti. 

Now, Fritz is grateful he found Project Citizenship and followed through with the naturalization process. He described his experience with Project Citizenship as “amazing, incredible, and outstanding.” 

“Whenever I needed you guys, you guys were there for me. If I [went]to the office, [you would] direct me to what I needed. You guys were always there for me.” 

Fritz attended one of Project Citizenship’s workshops to complete his application. “We talked, we listened, we learned, there was always someone there to help us out, I even passed your number to a couple friends.” 

Now a citizen, when Fritz thinks about the incredible work he has accomplished in Haiti and the beautiful life he has created in the United States, he feels proud at the coexistence of his two lives. When he hears the phrase ‘Welcome Home!’ he smiles and thinks about two countries instead of one. 

Testimonials
Read words of gratitude from individuals who have achieved U.S. citizenship with the support of Project Citizenship. These words reflect the appreciation of those we’ve had the privilege to assist.
“I want to thank the entire staff at Project Citizenship for the hard work that you have done for me. I am now a citizen and truly grateful for the help. Without your help, it wouldn’t be possible.”
Carl
Jamaica

Thank you to everyone for all of your help today. A very scary and nerve wrecking part of this process was made a little less scary. It feels extremely reassuring knowing that Project Citizenship is supporting my application. Immense gratitude! I hope to volunteer next year. ❤️”
Piseth
Thailand

“I first give thanks to God and then to you all. I passed my citizenship interview!”
Jenny
Dominican Republic

“To all who worked on my process from your team, thank you so much!!! I am now an American citizen and cast my 1st vote in this year’s election.”
Marie
Philippines

“My wife Hanifa and I would like to express to you and your colleagues at Project Citizenship our gratitude for your assistance, your kind welcome in your offices as well as your advice since the beginning of the citizenship application process.”
Mohammad
Algeria

“I want to thank you guys for making this process so easy and enjoyable for me. Thank you for all your help. I couldn’t have done it without you guys.”
Lya
Dominican Republic

“You guys helped me fill out the citizenship application form and I am very grateful for that. I went yesterday to my interview, and I passed, I was able to do the ceremony that same day as well. Thank you for everything!!”
Avigail
Dominican Republic

“We are so thankful for you all and your team for your help that you offered my parents. Today they achieved their dream of becoming American citizens thanks to your good work and dedication. We are so happy. Again, thank you and many blessings to everyone.”
Victor
Dominican Republic

“I passed the citizen test and now I am a U.S. citizen. Thanks for everything.”

Viola
Haiti

Staff:
Gail Breslow
Executive Director, French, Spanish, German

Gail joins Project Citizenship after 25+ years as Executive Director of The Clubhouse Network, a global network of community-based centers where young people from low-income neighborhoods explore their own interests, build skills, and develop confidence in themselves through the use of technology. Under her leadership the organization grew from a single location in Boston to more than 100 Clubhouses in 21 countries around the world. Earlier in her career Gail spent 12 years as a management consultant with Gemini Consulting and 3 years as a Senior Research Associate at the American Association for the Advancement of Science. She holds an MBA from Stanford Graduate School of Business and a B.A. from Oberlin College. As a granddaughter of immigrants, Gail is honored to be working in support of Project Citizenship’s mission and services on behalf of immigrants seeking U.S. citizenship.


Christine Burns
Communications Manager

Christine joined Project Citizenship as Communications Manager in January 2025, bringing over five years of experience in nonprofit communications and marketing. She has dedicated her career to mission-driven organizations that foster belonging, inclusivity, and connection. Growing up in Provincetown alongside immigrants whose hard work formed the backbone of the region’s seasonal tourist economy, Christine developed a deep appreciation for collaboration, community building, and storytelling. With a Bachelor’s Degree in Art History and Spanish from Wellesley College, she is thrilled to use her education and background to support Project Citizenship’s meaningful work of empowering immigrants on their journey to U.S. citizenship.


Maria Campaniello
Operations & Programs Manager

Maria joined Project Citizenship in September 2022, as a Communications & Operations intern. She recently graduated from Concordia University in Montreal, Quebec, with a Bachelor’s in Political Science. She also received a double minor in Human Rights and Immigration Studies. Maria is second generation, from her father who is an Italian Immigrant. This background has inspired her passion for social justice, and immigration services. She looks forward to her work with Project Citizenship and making a meaningful impact in her community by supporting naturalizing immigrants.


Adriana Céspedes
Program Assistant, Spanish

Adriana Céspedes is a Colombian attorney with extensive experience in human rights and immigration matters. Throughout her career, she has worked with vulnerable communities, including victims of armed conflict, supporting them in processes of comprehensive reparation and advocating for their fundamental rights.

As an immigrant herself, Adriana deeply understands the legal, social, and emotional challenges faced by individuals on their path to citizenship. Her professional experience includes advising families and communities on complex legal processes, ensuring compliance with transparency standards, and leading projects that promote inclusion and access to justice.

Committed to the mission of facilitating the integration and success of immigrants in the United States, Adriana combines her legal expertise and personal perspective to provide empathetic and effective support.


Stephanie Charles
Program Manager, Haitian Creole, French

Stephanie Charles is a growing and vibrant leader in the international development and immigration services space with a focus on non-profit management. As a Boston native, she holds a Bachelor of Arts Degree in International Studies and a minor in Theology from Boston College. She completed her graduate studies at Boston University’s Frederick S. Pardee School of Global Studies with a Master of Arts in Global Development Policy and a certificate in African Studies.

During her tenure at Boston College, Stephanie was recognized as a Ronald E. McNair scholar, where she conducted formal research on Iraqi and Somali refugee assimilation in the United States. Moreover, Stephanie’s career in the field stems from being a first-generation Haitian-American and from volunteering as a teacher’s assistant with a non-profit organization that supported recently immigrated children as they resettled in Boston. Stephanie continues to remain passionate about serving immigrant and international communities in the Greater Boston area.


Mossamed Chowdhury
Commonwealth Corps Service Member

Mossamed has joined Project Citizenship to fulfill her 10-month service year with the Commonwealth Corps. She graduated with a bachelor’s and a master’s degree in international relations. Throughout graduate school, she developed a particular interest in human rights issues, one aspect of which was understanding the challenges immigrants/refugees face. This led to her joining Project Citizenship where she hopes to give back to the community while helping immigrants with their naturalization process.


Lissa Damus
Program Coordinator, Haitian Creole, French

Lissa Damus joined Project Citizenship in September 2020. She graduated at the University of Massachusetts Boston with a degree in International Relations. She is currently pursuing her master’s International Relations as well. Lissa speaks Haitian Creole, French and English. Her interest in immigration comes from the fact that she and her parents are immigrants from Haiti. She understands the importance of getting citizenship and is passionate about helping others accomplish that goal.

 

 


Daniela Del Portillo
Program Assistant, Spanish

Dani Del Portillo joined Project Citizenship in 2025 as a Project Assistant. She is currently pursuing a B.A. in Fine Arts with a minor in Education at the University of Rhode Island. Born in Mexico and fluent in Spanish, Dani’s experience as an immigrant, alongside her mother’s, has deeply influenced her passion for social justice. These personal experiences have shaped her professional goal of serving the migrant community. 

Gloria Donati
Senior Staff Attorney, French, Italian

Gloria joined Project Citizenship in September 2020 as an AmeriCorps Legal Advocate of Massachusetts. Holding American and Italian citizenships, while also being of Ethiopian descent and having lived in several countries abroad, Gloria understands the importance of supporting immigrant communities in achieving their goals. Gloria earned a dual Bachelor’s degree in Italian and French laws from the University of Bologna and the University of Nanterre, as well as a Master’s degree in law from the University of Bologna. She recently graduated with an LLM degree from Boston University School of Law.
New York Bar License. 


Sneha
Hulagammanavar
Hindi, Marathi, and Kannada

Sneha joined Project Citizenship in June 2023 as a program assistant. She has more than 9 years of experience working with large financial institutions like Barclays, HSBC and Morgan Stanley and holds a bachelor’s degree in business administration. She migrated from India to the United States and eagerly seeks to contribute her skills to further the mission of Project Citizenship.


Michael Lacek
Access to Justice Fellow

Michael retired in 2018 after serving as a litigator, regulatory lawyer, and transactional lawyer for Met Life, Inc. for almost 20 years. Upon graduation from Columbia University School of Law, where he was the Executive Editor of the Columbia Journal of Law and Social Problems, Mike began his legal career as an Associate at Cravath, Swaine & Moore in New York. Upon moving to Boston, he joined the Litigation Department at Palmer & Dodge as an Associate and then Partner, where he worked on a wide variety of litigation and transactional matters. In retirement, Mike now volunteers at Newton Wellesley Hospital and the Wellesley Council on Aging. As an Access to Justice Fellow, Mike will partner with Project Citizenship to educate immigrants about the benefits of citizenship and to assist eligible, legal permanent residents to overcome barriers to naturalization.


Elsa Laskorski
Staff Attorney, Spanish, Finnish

Elsa Laskorski joined Project Citizenship in November 2023 as a Staff Attorney. Elsa earned her law degree from Roger Williams University School of Law, where she spent her final semester working as a student attorney in the school’s Immigration Clinic. Prior to law school, she spent several years working in immigration legal services in Providence, Rhode Island. A dual citizen of the United States and Finland, Elsa’s own family inspired her commitment to helping immigrants, and she looks forward to continuing that work at Project Citizenship.


Francelia Lievanos
Legal Services Intern, Spanish

Having been an undergraduate program intern in the summer of 2019, Francelia rejoined Project Citizenship in May 2024 as a legal intern. Since the summer of 2019, Francelia graduated from Pitzer College with a degree in Political Science & Chicanx/Latinx studies, worked in housing-related matters, and gained experience in various immigration fields, including removal defense and employment-based immigration. Currently, Francelia is in her 3rd year at New England Law | Boston, where she is concentrating on immigration law. Being an immigrant herself, Francelia is passionate about Project Citizenship’s mission and helping others navigate the complexities of the immigration system.


Heather Monty
Development Director

Heather joined Project Citizenship in 2023 as the Development Director. She has a decade of experience in nonprofit fundraising and communications, working to actively build thoughtful relationships, foster collaborative thinking, and communicate need and impact through strength-based storytelling. She graduated from Bates College with degrees in Anthropology and Women and Gender Studies, and she strives to leverage her educational, personal, and professional experiences to encourage inclusive and equitable community engagement and opportunity.


Alex Orellana
Program Assistant, Spanish

Alex Orellana joined Project Citizenship in December 2023 as a program assistant. He is currently a student at the University of Massachusetts Boston pursuing a degree in Business Management, with a concentration in leadership and organizational change. Fluent in Spanish and second generation, Alex draws inspiration from his parents’ naturalization to help others on their journey to citizenship. Alex looks forward to making a difference in his community and hopes to help others navigate the naturalization process.


James Richardson
Staff Attorney

James Richardson joined Project Citizenship in the Summer of 2021 as an AmeriCorps Legal Advocate of Massachusetts.  James recently graduated from Suffolk University Law School where he was certified as a student attorney and worked in Suffolk’s Housing Clinic.  It was there, that he became interested in public interest law. Prior to law school, James studied political science and history at the University of Massachusetts, Amherst.


Marissa Rodriguez
Associate Director

Marissa Rodriguez is the Associate Director at Project Citizenship. In this role, she oversees internal operations, supports the fantastic staff team, and aids in setting the strategic direction of the organization. Marissa comes to Project Citizenship with a wealth of experience in the social sector, including roles focused on staff learning and development, curriculum and program design, operations and project management, educational technology, and experiential learning. Marissa received a B.A. in Letters, Arts, and Sciences from Penn State University and an M.Ed. with a concentration on eLearning & Instructional Design from Northeastern University. She is excited to bring her robust skillset to the Associate Director role with the aim of empowering staff and supporting clients to further the mission of Project Citizenship.


Khadeja Usmani
Program Assistant, Spanish, Urdu, and Hindi

Khadeja Usmani joined Project Citizenship in September 2024 as a Program Assistant, blending her academic focus on political science, international relations, and pre-law studies at Boston University with her personal connection to the immigrant experience. As the daughter of Pakistani immigrants, Khadeja is deeply invested in helping others navigate the path to citizenship. Fluent in Spanish, Urdu, and Hindi, she offers both linguistic and cultural understanding to her clients. Khadeja’s commitment to social justice and her pre-law aspirations drives her passion for advocating for immigrant rights and supporting underrepresented communities in their journey towards citizenship. 


Madeleine Votaw
Commonwealth Corps Service Member

Madeleine is a recent graduate of the University of Exeter with a bachelor’s degree in anthropology and has joined the programs team at Project Citizenship as one of the two 2024-2025 Commonwealth Corps service members. As a dual citizen of the United States and the UK, she understands the importance of Project Citizenship’s mission and strives to help immigrants living in her new local community.

Board:
Milton Manousaridis
Chair

Milton is Vice President and Relationship Manager at JP Morgan Chase. He acquires, develops, and maintains a successful portfolio of relationships while offering unparalleled banking service at all levels. He prides himself in providing banking service along with value to businesses, private clients as well as non-profit verticals.

Milton received his B.A. in Industrial Psychology/Organizational Behavior from the University of Massachusetts, Boston. Even though he calls Boston and the Metrowest his home, he does not forget his Hellenic roots and what it means to be an immigrant. This is one of the driving reasons he has joined Project Citizenship.

In addition to multiple networking groups, he is a member of USA500 Boston Seaport.


Nandini Karkare
Vice Chair

Nandini Karkare is co-founder at UnStrange, a startup focused on rekindling the art of spontaneous conversations. Nandini has 18+ years of experience driving operational efficiencies and building organizations to support consistent growth. For the last 15+ years, Nandini was with EDB, a global software company with employees in over 40 countries around the world and customers in more than 80 countries, where Nandini played various leadership roles, including most recently being nominated Chief-Of-Staff to the CEO. Her international team of Operations & Analytical professionals built a strong foundation of automated business practices and plans, resulting in 54+ quarters of recurring revenue growth for EDB. Nandini has a BA in Psychology from Pune University, India, and is a naturalized citizen of the United States. She has raised a child as a single mother across continents and has empathy for the challenges immigration can bring to an individual’s life.


Scott Posnick
Treasurer

Scott Posnick is a retired Director & Consulting CFO in AAFCPAs’ Outsourced Accounting and Fractional CFO practice. Prior to his time at AAFCPAs, he spent his career working in a variety of industries providing high-level CFO oversight and strategic planning, including financial forecasts & analysis and advising on growth strategies, business transactions, tax optimization, and strengthening internal controls. Scott took pride in providing trusted guidance, responsiveness, and clear communication to companies and their owners/shareholders at various stages of growth. He received his MBA from Suffolk University Sawyer School of Business and his BS from Babson College. As the grandson of immigrants, he is passionate about the importance of immigration, citizenship, and the mission of Project Citizenship.

 


Natalia Ivanytsky
Clerk

Natalia is the Director of Global Accounting at Converse Inc., a subsidiary of Nike Inc. At Converse, Natalia oversees a team of accountants and is primarily responsible for external financial reporting, technical accounting, tax and treasury operations. She is a CPA and a graduate of Boston College with a Bachelor of Science in Accounting and a minor in International Studies. Natalia was born in Lviv, Ukraine and emigrated to the United States with her parents in 1993. She studied abroad in Madrid, Spain and did a secondment to Melbourne, Australia with her previous employer, PwC, for three years. Natalia lives in Charlestown with her fiancé, Ryan, and their adopted dog Kali, who was rescued from a shelter in Little Rock, Arkansas. Natalia previously volunteered with the immigration department at the International Rescue Committee office in Boston, MA and has volunteered her time on various small consulting-type projects while at PwC with different not for profit organizations.


Heidy Abreu King-Jones
Heidy Abreu King-Jones is Chief Legal Officer and Corporate Secretary of Spyre Therapeutics. From 2020-23 she held the same roles at Provention Bio, leading the legal support for the eventual sale of the company to Sanofi.  Before that she served as General Counsel and Corporate Secretary of Axcella Health and managed the Corporate and Commercial Law Department at Sarepta Therapeutics. Heidy began her legal career at Ropes & Gray, where she represented public companies in corporate matters including mergers, acquisitions, corporate governance issues, and SEC filings. She also represented pro bono clients on asylum, immigration, medical and housing matters.  Heidy was raised in New York City and was a first-generation college student at Dartmouth and then received a law degree from Cornell. She helped her mother and many friends and family members naturalize while she was still in college, and is deeply committed to Project Citizenship’s work on behalf of immigrants, in particular those from marginalized backgrounds. Heidy also serves on the board of directors of the Greater Boston Food Bank. She lives in the Boston area with her husband and daughter.


Tref Borden
Tref Borden is the former Executive Director of the Fish Family Foundation, a Boston-based private foundation focusing primarily on human services for low-income individuals and families in the Greater Boston area, with a particular interest in immigration and naturalization programs.  As Executive Director of the Foundation, Ms. Borden worked closely with its Investment Committee managing the foundation’s assets in addition to managing the Fish Family Office.

Prior to coming to the Fish Family Foundation, Ms. Borden had served as Executive Director of the Tiger Foundation in New York City. The Tiger Foundation supports educational, vocational, and social services organizations focusing on the lowest-income, highest-risk populations in the city.  Ms. Borden left the Investment Banking field to join Tiger as its founding Executive Director.

Ms. Borden has served 10 years on the Philanthropy Massachusetts Board, formerly as chair.


Christopher Henry
Chris Henry is a Partner in the Boston office of Latham & Watkins, representing clients in high-stakes trade secret and patent litigation before US district courts, the US Court of Appeals for the Federal Circuit, the Patent Trial and Appeal Board, and the US International Trade Commission. He represents high technology clients in intellectual property litigation involving a wide variety of technologies, including software, electromechanical devices, medical technologies, and semiconductors. He draws on trial experience and strong oral advocacy skills to help clients obtain multi-million-dollar settlements, summary judgment and trial victories, and other favorable resolutions. Christopher clerked for Judge Henry Coke Morgan Jr. in the US District Court for the Eastern District of Virginia and served under Magistrate Judge Mary Pat Thynge in the US District Court for the District of Delaware. 


Benny Omid
Benny Omid was born in Iran, immigrated to Boston in 1988 and became an American Citizen in 1996. Benny began his career with Dunkin’ Donuts 35 years ago, on the ground floor cleaning stores. Through determination and hard work, in 1996, Benny became a Dunkin’ Donuts franchisee and now owns restaurants in Allston, MA. Benny is a Director at the Massachusetts Region of the American Red Cross and the Chair of the Biomedical Committee. Benny was the Northeast Co-Chair and Treasurer of The Dunkin’ Donuts and Baskin-Robbins Community Foundation and a director at the American Red Cross Biomedical Services, where he had been an integral part of the “Dunkin’ Donors Make a Difference” campaign. He was also a member of the Dunkin’ Donuts Advertising Committee for the Northeast Region and the Vice Chair of the Allston Board of Trade. Benny lives in Belmont with his wife Margarite and his son Jacob. 


David Rangaviz
David Rangaviz is an Assistant Attorney General in the Civil Rights Division of the Massachusetts Attorney General’s Office. He previously worked as an appellate staff attorney at the Committee for Public Counsel Services (CPCS), and a trial attorney in the Maryland Office of the Public Defender. He currently serves as a member (and former co-chair) of the Boston Bar Association’s Criminal Law Section and as a participant in the Harvard Kennedy School’s Roundtable on Racial Disparities in Massachusetts Courts. Dave also teaches at Boston College School of Law, where he focuses on criminal law and procedure. His scholarship has appeared in the Boston College Law Review, American Criminal Law Review, and Harvard Civil Rights-Civil Liberties Law Review, among others. Following law school, Dave clerked for Kent Jordan of the U.S. Court of Appeals for the Third Circuit, Barbara Lenk of the Massachusetts Supreme Judicial Court, and John Conroy of the U.S. District Court for the District of Vermont. He is a graduate of Brown University and Harvard Law School. As the son of an Iranian immigrant who became a naturalized citizen, Dave cares deeply about the mission and work of Project Citizenship. He lives in Cambridge with his wife and two boys (with a third on the way!).


Simon Ringrose
Simon is an experienced financial services sales professional who became a US citizen in April 2017 and lives in Charlestown. Simon has worked for the UN World Food Programme in China and for Reuters in London, Nicosia, and Boston. Currently employed by Quant Insight, a UK-based financial data and analytics start-up, Simon worked previously at EPFR Global, a Cambridge-based financial data startup sold to Informa Plc. He has a deep interest in news, the investment process, and global markets.

Active in community affairs Simon volunteers weekly with St Marks US Citizenship classes and with East Boston’s Allies for Immigrants ESOL classes.  He is currently on the Vestry at St John’s Church, Charlestown and has taught children’s religious education classes there for 15 years. Married with three children, Simon studied at Tufts, Beijing Normal University, and the London School of Economics. In his free time he enjoys kayaking at Belle Isle and hiking in the New England outdoors.


Katherine Rivet
Katherine Rivet works for Boston Consulting Group as their Global Director of Career Development, a role she has held since 2019. She is passionate about talent development and support for diversity, with professional experience working in Mexico, Brazil, and the US.

In addition, Katherine has actively worked to support internal efforts to promote work-life sustainability (hosting a successful internal podcast focused on personal balance and sustainability) as well as diversity and inclusion (as a member of the Global Services Inclusion Accelerator team). She is an active Dartmouth alum, serving on Tuck Business School’s Latin American Board from 2011-2013.

She received a BA in International Relations with a minor in Latin American Studies from Tufts University and an MBA from The Amos Tuck Business School at Dartmouth College. She lives near Boston with her husband Cesar, their children Santiago and Sofia, and their beloved dog Francisco Lopez (aka Pancho).She is fluent in Spanish and is conversant in Brazilian Portuguese.


Detlev Suderow
Detlev Suderow is the retired Senior Vice President of Human Resource and Organization Effectiveness for FLIR Systems, Inc.  FLIR is an infrared technology company with global operations listed twice among Business Week’s 100 fastest growing companies.  Prior to joining FLIR Systems, Detlev served as Vice President of Human Resources for Inframetrics, a fast growth start up technology company.  His career includes his role as the Human Resource Manager for CLARiiON, the entrepreneurial business division of Data General Corporation, and a thirteen year career at Digital Equipment Corporation as H.R. Manager, Organizational Development Manager, and Training and Development Manager.

Detlev considers himself fortunate enough to have capped his decades-long business career with a pivot to academia: as Professor of the Practice and Senior Lecturer at the International Business School, Brandeis University.  Here he served as the career advisor for the undergraduate business program and counseled graduate students at the International Business School. He co continues to serve on numerous Brandeis University committees and boards.

For Detlev, an immigrant himself (Germany), US Citizenship is a gift that keeps on giving, and one that brings him enthusiastically into the Project Citizenship fold. He holds degrees from Brandeis University (BA), Tufts University (MA) and The University of Zurich. Together with his immigrant wife (Canada) he is the parent of two first generation sons.

Advisors and Ambassadors:
Elizabeth Amador
Elizabeth is a SNAP Supervisor at the Department of Transitional Assistance, and serves as the Community and Homeless Liaison for her office in Boston.  With an Associate’s degree in Human Services from Bunker Hill Community College, and a Bachelor’s degree in Human Services from Northeastern University,  Elizabeth is passionate about helping others. She is an Activist, Influencer, and Community Leader for the Latino Community of Massachusetts with a goal to make sure her community is well informed of services, resources, and opportunities. She is devoted to making sure those who are ready and eligible to become US Citizens complete their application and become a part of the voting process. Elizabeth was born in the Dominican Republic and moved to New York City at the age of 8. She naturalized in 1999 when she moved to Boston, MA where she still resides, married with three children.


Talia Azzaretto
Talia Azzaretto is an associate attorney at Burns & Levinson LLP, focusing on estate planning as well as estate and trust administration. She enacts sophisticated planning strategies tailored to her clients’ goals and strives to educate her clients throughout the planning and administration processes. She holds a J.D. from Benjamin N. Cardozo School of Law, and a B.B.A., summa cum laude, from Loyola College in Maryland. In her spare time, Talia enjoys getting outside in nature with her husband and two young children.


Jake Benhabib
Jake is an immigration and human rights lawyer based in Brooklyn, New York. He is currently a staff attorney at the International Rescue Committee. Previously, he was a staff attorney at Catholic Charities, and a staff attorney and legal fellow at Project Citizenship. He has a JD with Honors in the Concentration of International Law from Boston University, and a BA, magna cum laude, from Rutgers University. Jake is the son and grandson of former refugees from Cuba, and the great-grandson of Sephardic Jewish immigrants from Turkey. He served as a Peace Corps volunteer in Kyrgyzstan, and speaks conversational Kyrgyz and Spanish.


Karen Bobadilla
Attorney Karen B. Bobadilla is a dual licensed attorney, in Massachusetts and in Peru. She obtained her LLM with a concentration in Human Rights at Northeastern University School of Law. She is one of the immigration attorneys at De Novo in Cambridge, MA. Her practice focuses on domestic violence survivors, victims of crimes and on Special Immigrant Juvenile cases -in the Probate and Family Courts, USCIS and the Immigration Court. Before becoming an attorney in the U.S., she was one of the few DOJ Full Accredited Representatives in Massachusetts.

In addition to her work at De Novo, she volunteers at the Massachusetts Association of Hispanic Attorneys (MAHA) as a board member, at the American Immigration Lawyers Association- New England Chapter as the Probate and Family Court liaison. She is an active member at the Boston Bar Association. She is a member of the BBA’s Immigration Law Section Steering Committee and New Lawyers Forum and volunteers as a coach for the BBA’s Bar Exam Coaching Program and is part of the BBA Public Interest Leadership Program Class of 2023.


Ed Boyajian
Chair Emeritus

Ed is Chairman of the Board of Directors at EDB, a global software company with employees in over 40 countries around the world and customers in more than 80 countries. Ed leads the development and execution of EDB’s strategic vision and growth in the database industry. He joined EDB in 2008, and has since steered the company through 50+ consecutive quarters of growth. He is known for his passion, relentless energy, and strategic leadership. Prior to his business career, Ed honed his leadership skills as a Captain in the U.S. Army. He earned his MBA from Harvard Business School and BA from Boston University. Ed is also the proud grandson of Armenian immigrants.


Tiffany Brathwaite
Tiffany is the office manager for the Boston Celtics headquarters where she has been for the past 4 seasons.  Along with the many hats she wears in her current role, in 2020 she became the pilar lead for the Voting and Civic Engagement Committee under the newly formed social justice initiative of the company called Boston Celtics United.  Previously, she was a personal chef for several years and taught baking classes for middle and high school students in Lexington MA.  Tiffany became very passionate about naturalization when going through the process with her dad who was a permanent resident for over 30 years.  By seeing firsthand the sometimes difficult and long process made her think of others who don’t have the help her dad had and became very passionate about breaking down barriers for people in need. In her free time, Tiffany enjoys cooking for fun, baking bread, reading a good book and weekend getaways.


Juan Davila
Juan is a Senior Vice President at Bank of the West working in their corporate group where he works in helping large corporate clients define their financing strategies. He has 30 years of experience in international Banking leading teams on diverse areas of Risk Management and was previously Chief Risk and Credit Officer for Santander.

Juan and his wife Susana are first-generation immigrants and became US citizens in 2015. They recently moved with their 3 children to San Francisco after 10 lovely years in Boston where he was a Board member at Project Citizenship

He is a graduate of ICADE (Madrid) and Middlesex University (London) and a Harvard Business School Alumni.


Brenda Diana
Chair Emeritus

Brenda is a partner of Ropes & Gray, in the firm’s Private Client Group. She serves as trustee of numerous trusts, represents fiduciaries in the settlement of estates, and prepares estate plans for individuals. Brenda works with multiple generations of families with accumulated wealth, entrepreneurs, private and public company executives and shareholders, and professional public personalities, and other high net worth clients. Her practice involves the administration of client estates and trusts, including post-mortem tax planning and giving advice regarding fiduciary responsibilities. Brenda serves as executor for estates of varying size and complexity, helping clients through diverse personal transitions and providing advice on risk management, fiduciary investments and efficient tax alternatives to avoid potential issues or disputes. In addition, she coordinates the proper disposition of individual and family assets including art, antiques, real estate, and other valuables and works with well-known auction houses and advisors when appropriate. Brenda’s practice also involves estate planning, including advising clients on various charitable and philanthropic endeavors. She works closely with financial planners and philanthropic advisors to develop comprehensive plans to meet the unique needs of her clients. Brenda has a J.D. from New York University School of Law and a B.A. from Cornell University.


Susan Eaton
Dr. Susan Eaton is Professor of Practice in Social Policy and Director of the Sillerman Center for the Advancement of Philanthropy at Brandeis University’s Heller School for Social Policy. At the Sillerman Center, Susan and her colleagues engage funders and their advisors, socially concerned scholars and non-profit practitioners to increase and enhance grantmaking to social justice causes.

Susan is an author, most recently, of the book, Integration Nation: Immigrants, Refugees and America at Its Best (The New Press, 2016), about myriad efforts that welcome and incorporate immigrants into their new communities across the United States. She also is the author of the critically acclaimed, The Children In Room E4: American Education on Trial (Algonquin, 2007), which chronicles a landmark civil rights case and life in a classroom and neighborhood in Hartford, Connecticut and The Other Boston Busing Story: What’s Won and Lost Across the Boundary Line (Yale, 2001), a qualitative interview study of the adult lives of African Americans who had participated in a voluntary school desegregation effort in suburban Boston. She is co-author, with Gary Orfield, of Dismantling Desegregation: The Quiet Reversal of Brown v. Board of Education. (New Press, 1996).

Prior to her appointment at Heller in 2015, Susan was research director at the Charles Hamilton Houston Institute for Race and Justice at Harvard Law School and an adjunct lecturer at the Harvard University Graduate School of Education. While at Harvard, Susan founded and co-directed the storytelling project One Nation Indivisible, which amplifies the voices and work of people creating and sustaining racially, culturally and linguistically integrated schools and other social institutions.


Deva Hirsch
Deva Hirsch is an accomplished philanthropic and nonprofit professional with local, national and international leadership experience. She is Executive Director of the Rich Foundation in Atlanta, Georgia. Deva previously served as Executive Director of the Paul & Phyllis Fireman Charitable Foundation in Boston, the Executive Director of the Abraham J. & Phyllis Katz Foundation in Atlanta and as Co-Director and Vice President for Program at the Arthur M. Blank Family Foundation.  Deva is the Founder and President Emeritus of Hands on Tokyo, a cross-cultural clearinghouse matching corporate and volunteer interests with community needs. She serves on the Board of Directors for the Atlanta Music Project and the Advisory Committees for GreenLight Fund Atlanta, Project Citizenship and the U.S.-Japan Council. Deva has an MA in Urban and Environmental Policy and Nonprofit Management from Tufts University and a BA in Journalism and Public Relations from the University of Georgia.


Garey House
Garey is a Business Development Manager for JPMorgan Chase in Boston, MA. With over 14 years of experience in financial services, Garey has a demonstrated expertise in helping businesses utilize technology strategically to improve cash flow, mitigate risk and to scale the growth of their companies.  He is passionate about financial technology and has a certification as a Treasury Professional with AFP and an accreditation as an ACH Professional with NACHA. He graduated with a BA in Sociology from the University of Missouri and is currently completing his MBA with a focus in Analytics at University of Massachusetts-Amherst. Outside of work, Garey enjoys going on long walks with his wife and is passionate about giving his time to several philanthropic initiatives within this community and the Greater Boston area.


Andy Liebman
Andy Liebman is award-winning filmmaker, software entrepreneur, and political activist. Having graduated from Tufts University with a bachelor’s degree in philosophy, he began his career in the early 1980’s as a producer, director, writer and editor of documentary and docudrama films for PBS and the Discovery Channel – including many episodes of Frontline, NOVA, Scientific American Frontiers, Race to Save the Planet (environment), and The Secret of Life (genetics).  He won the duPont Columbia award for excellence in journalism as well as multiple national Emmy awards for his ground-breaking work covering science, history, nature and politics. While producing a Discovery Channel series that was following a simulated human mission to Mars and that was being shot and edited by a team of people in below freezing weather in the Canadian Arctic, he conceived of technology that would enable a group of directors, video editors and assistants to work collaboratively (a problem he faced in this particular production), leading to the founding of EditShare.

Andy served as CEO of EditShare for 15 years, and his vision for how technology could fuel collaboration and bring efficiency to production had a major impact on the way television programs and films were made around the world.

As Andy stepped back from EditShare, he got involved in politics and worked diligently during the 2020 election cycle to get out and protect the vote.  Using his organization, technology, and communication skills, he helped recruit and manage a small army of phone bankers and letter writers. Moving forward, Andy plans to stay involved with political and social activism.  He is also currently establishing a new nonprofit that’s focused on getting fiction and non-fiction media to become a more constructive force in the world.


Bill Lundin
Bill is a Senior Associate with Fragomen, Del Rey, Bernsen & Loewy in Boston, MA, where he has practiced immigration law for seven years. He developed an interest in immigration law, and in the pathway to U.S. residency and citizenship more specifically, through study of Mandarin Chinese in Beijing, teaching kindergarten at a predominantly Somali-American charter school in Minneapolis, and completing assignments abroad in Kochi, India and Shanghai, China. Bill is the pro bono coordinator for Fragomen’s Boston office and has taken an active role in strengthening the office’s pro bono program, and looks forward to continuing to grow the partnership between Fragomen and Project Citizenship with his Fragomen colleague on the A&A Board, Kelly Renaud. In his free time, Bill enjoys outdoor activities, especially long-distance bike trails, cross-country skiing and is an avid fan of the U.S. men’s national soccer team (looking forward to seeing matches at Gillette Stadium in 2026!).


Jennifer Jean-Michel
Jennifer is Corporate Counsel at Cognex Corporation, a public technology company in Natick, Massachusetts, where she specializes in securities filings, M&A, ESG, commercial agreements and sales to the life sciences industry. Jennifer was previously a Corporate Associate at DLA Piper LLP where she represented public and private companies in equity financings, mergers and acquisitions and corporate governance matters. Jennifer is a dedicated pro bono attorney and has volunteered for a number of local immigration organizations, including Project Citizenship. She holds a J.D. from Boston University, and a B.S., magna cum laude, from Boston University. In her free time, Jennifer enjoys cuddling with her two cats, exploring local bike trails and getting in an exercise class.


Jim McGarry
Jim is a partner in Goodwin Procter’s Consumer Financial Services Litigation Group who specializes in complex commercial litigation, with an emphasis on the defense of financial institutions in consumer class actions, enforcement actions and complex business litigation. As a member of this practice, Jim has defended against state and nationwide class actions and multi-district class actions around the country. His work has covered a wide variety of consumer class actions and government investigations facing the financial services industry, including banks and mortgage servicers in a host of challenges to mortgage servicing, fair lending and predatory lending practices and auto lenders in loan origination and servicing matters.  Jim is a member of the American, Massachusetts and Boston Bar Associations, and has written and spoken on a variety of topics pertaining to financial services and class action litigation. He attended Seton Hall University where he obtained his B.A. in 1985 magna cum laude. He graduated from Rutgers School of Law in 1993 magna cum laude. He is a former member of the Board of Directors of the Massachusetts Appleseed Center for Law and Justice. Jim is married with two teenage daughters, both of whom have also volunteered for Project Citizenship.


Mike McGurk
Mike McGurk has over 30 years of experience in virtually all aspects of patent law. Working with clients ranging from small start-ups to large Fortune 100 companies, he provides counsel in due diligence matters, global portfolio development and adversarial proceedings. Mike’s practice is informed by his background as a patent examiner for the USPTO, as a litigator for ten years, and as an expert in due diligence matters large and small. His extensive due diligence experience includes pre-litigation, acquisition, in-license, freedom-to-operate product and/or process clearance, design around, validity and patentability matters. Mike works primarily in the pharmaceutical, chemical, medical device, clean energy and mechanical technologies.


Amilcar Navarro
Amilcar is a Director for the Cybersecurity, Privacy and Forensics practice at PricewaterhouseCoopers (PwC). He has been focused on helping organizations understand and effectively manage cybersecurity risks. He holds a System Engineering degree, as well as an MBA from Hult International Business School and other post-graduate studies and certifications in the cybersecurity field such as CISSP and CISM. Amilcar has had the opportunity to learn about different cultures thanks to having work responsibilities across multiple countries in Latin America. As an immigrant since 2014, he faced many challenges before getting a permanent residence card so he can relate to the stress that it comes with. He is always lending a hand and sharing what he has learned to others that arrive new to the country. Amilcar enjoys the beach, and he is big into boating.     


Carolyn Osteen
Carolyn is a retired partner with the Boston office of Ropes & Gray LLP and was a member of its tax department. She joined the firm in 1970 and her practice has focused on exempt organizations, including representation of a number of colleges, universities, museums, and hospitals. She speaks regularly on issues of charitable giving and tax and corporate problems of tax exempt organizations. Carolyn is the co author of the “Harvard Manual Tax Aspects of Charitable Giving” last published in its 9th Edition as well as co author of the BNA portfolio, “Charitable Contributions for Corporations.” She has served as a member of the Massachusetts Attorney General’s Public Charities Advisory Committee. She has served as a Fellow of The American College of Trust and Estate Counsel, as a Regent of the American College of Tax Counsel and on the Governing Council of the Tax Section of the American Bar Association. She has also chaired the Exempt Organizations Committee of the Tax Section. Carolyn is an alumna of Wellesley College and holds LL.B. and LL.M. degrees from Duke University School of Law, where she serves as a member of the Board of Visitors. Carolyn is an emeritus trustee of the Boston Athenaeum and serves as a Trustee of Boston Preparatory Charter School’s support foundation. She has served as a trustee of many New England non-profit organizations and continues to work in a volunteer capacity with various non-profit organizations including The Trustees of Reservations, Historic Boston, Incorporated, and Native Plant Trust. Carolyn is married to Robert T. Osteen, M.D. (B.A., Dartmouth College), and has two daughters.


O’Neil Outar
O’Neil A.S. Outar is the Executive Vice President of Advancement for The Greater Boston Food Bank (GBFB), overseeing communications, fundraising, marketing, and public affairs. Prior to joining GBFB, O’Neil spent 30 years in senior fundraising and engagement management roles at Rhode Island School of Design, the University of Pittsburgh, Harvard University, the University of Alberta, MIT, and Tufts University. Among his accomplishments, he has led or played leadership roles in campaigns ranging from $9 billion to $500 million and established the fundraising framework for signature programs in cancer research, energy, global partnerships, graduate education, and student leadership development. Currently a Special Adviser to The Guyana Foundation, a member of the Advisory Board for the Harvard Data Sciences Review, and an Advisor to Project Citizenship, O’Neil was a past member of the Board of Directors for Project Citizenship, trustee of the Council for the Advancement and Support of Education, a Commonwealth Study Conference Leader, a Ditchley Scholar, a member of the World Economic Forum’s Knowledge Advisory Group, and an MIT Leader-to-Leader Fellow. A first-generation college graduate, O’Neil was born in New Amsterdam, Guyana, and is named in honor of his father’s favorite Australian cricketer, Norman O’Neill. He was educated in Brooklyn (N.Y.), New Hampshire, and Massachusetts and holds a Master of Arts in Urban and Environmental Public Policy and a Bachelor of Arts, both from Tufts University.


Kelly Renaud
Kelly is a business immigration attorney advising organizations of all sizes. She has extensive experience with complex applications for professionals in the EB1 and O-1 classifications in the biotech and life sciences industry. She is currently an associate with Fragomen in their Boston office and has volunteered with Project Citizenship and other local immigration non-profits representing folks in bond and removal proceedings, participating in citizenship clinics, and providing informational sessions following immigration policy changes. Kelly is a member of her firm’s Diversity, Equity, and Inclusion network, the American Immigration Lawyers Association (AILA), the Massachusetts and American Bar Association, and in her spare time enjoys learning languages and trying new whole food plant-based recipes.


Janet Rickershauser
Janet Rickershauser counsels nonprofit organizations on a broad array of governance and tax issues and works with individuals and families on charitable giving strategies such as creating a family foundation or making an endowment gift.
As an experienced estate and tax planning attorney, Janet counsels individuals and families on complex estate planning and charitable giving strategies, such as creating and administering family foundations, establishing charitable remainder trusts, and making endowment gifts.
Janet holds a J.D. from New York University School of Law, an M.A. from Columbia University, and a B.A., magna cum laude, from Brown University, and she speaks French and some Russian and Spanish. 


Seth Rolbein
Seth Rolbein began his career as a journalist on Cape Cod in the 1970s. He then joined WGBH-TV in Boston as a writer, reporter and documentary filmmaker, also writing for many regional and national publications, including The Boston Globe Sunday Magazine. His magazine and book-length fiction and non-fiction has spanned many topics (and continents), and his documentaries on National Public Television have won multiple national awards. Throughout, the Cape has been his home; he became editor-in-chief of the region’s weekly newspaper chain before starting The Cape Cod Voice. He then served for six years as chief of staff and senior adviser for Cape and Islands Senator Dan Wolf, translating a journalist’s perspective into public policy initiatives. Seth then joined the Cape Cod Commercial Fishermen’s Alliance as head of the Fisheries Trust and Senior Policy Adviser. He works with community members, state and federal officials, and like-minded organizations. “Connecting the dots” as he likes to say, bringing people together, understanding how decisions are made, who has a say, and who benefits, are his main interests.


Nancy Rousseau
Nancy Rachel Rousseau, a Haitian-American, has lived in Massachusetts for twenty-five years. Focused on rebuilding community, Ms. Rousseau has committed her life to helping others advance their own lives and serving as a bridge to resources. She believes community will improve as each person – young and old – is empowered to do more. Nancy is Founder of Cultivate Womanhood, Inc. – home to the Boston’s Next Top Model Summer Program, a confidence-building program for girls, which is currently under reorganization. She is a proud member of the Psi Iota Omega Chapter of Alpha Kappa Alpha Sorority, Incorporated, for which she serves as the 1st Vice President and Chairperson of the Connection and Social Action Committee.

Ms. Rousseau is a two-time graduate of Northeastern University. She holds a Master of Science in both Nonprofit Management and Leadership and a Bachelor’s degree in Finance and Management.


Alicia Rubio-Spring
Alicia is an associate in Goodwin Procter’s Business Litigation Group. She represents clients in a variety of complex litigation matters in both federal and state court, including general commercial litigation, post-closing disputes, and consumer financial services litigation. Alicia also dedicates a significant portion of her practice to pro bono immigration services, devoting particular attention to unaccompanied minors and asylum-seekers. Ms. Rubio received her B.A. from Georgetown University and her J.D. from Boston College Law School. She was thrilled to join the Project Citizenship board in 2016.


Charles Sanders
Charles is a partner in Latham & Watkins Litigation Department. He has market-leading, first chair intellectual property litigation experience.  Formerly with Goodwin Procter’s Intellectual Property Litigation Group, Charles focused on intellectual property matters with emphasis on patent litigation. He has represented clients in Asia, Europe and the United States as lead counsel in district courts throughout the United States and before the U.S. International Trade Commission. He has been named a Massachusetts Super Lawyer by Law & Politics and Boston magazines.  With a background in chemistry and physics, he has represented clients in a diverse range of technologies. Charles has also handled antitrust, false advertising, trademark infringement, trade dress infringement, and unfair competition claims. He is married with a daughter and an avid fan of baseball and basketball.  Charles is a frequent and dedicated pro bono volunteer for Project Citizenship.  He has volunteered at numerous workshops, and has provided many hours of pro bono service assisting citizenship applicants as well as a Board member.


Mary Teague
Mary is a Senior Vice President and Senior Legal Counsel at Santander Bank and its parent holding company in Boston, Massachusetts, where she serves as Deputy Corporate Secretary, advises the board and management on corporate governance matters, and supports the activities of the board, board committees, and executive management committees. Prior to her role at Santander, Mary practiced law at Cadwalader, Wickersham & Taft in New York, after which she worked at an advisory firm outside of Boston and facilitated education sessions for Fortune 500 directors regarding emerging corporate governance matters.  Mary earned a J.D. from Boston University and a B.A. from Kenyon College. She lives in Massachusetts with her husband and three children –  and their cat and dog who are diligently trying to understand one another.


Melanie Torres
Program Manager at The Klarman Family Foundation. Prior to her role at The Klarman Family Foundation, Melanie worked at Project Citizenship for over 6 years, ultimately serving as Deputy Director. Melanie holds a BA in International Relations from Boston University and has served on the Commission for Immigrant Rights and Citizenship in the City of Cambridge. When she isn’t working, or training her puppy, Melanie can be found playing or watching soccer with friends and family.


Luis Vélez
Luis Vélez is a lawyer and professor at the Sergio Arboleda University School of Law in Bogotá D.C. He is a graduate of the John Jay College of Criminal Justice in New York City; advanced studies in Social and Criminal Justice at Boston College. Luis Vélez has a master’s degree in Criminal Law and Criminology from the Externado de Colombia University. He is Doctor Honoris Causa, Ibero-American Doctoral Cloister of Mexico. Former “faceless” judge and prosecutor in Colombia. He was Director of Investigations of the Office of the Attorney General in Bogotá D.C. and Cali. Additionally, he was Academic Director of the School of Judges in his country. He worked as a researcher at CICIG, at the UN, in Guatemala. He worked with the Secretary of Transparency of the Presidency of Colombia. He is a consultant in Mexico on the rights of victims and the fight against the crime of forced disappearance. He is the author of various publications. He worked with Citizenship Now in New York City and with Service Employees International Union (SEIU) in Boston.


Amy Wax
Amy M. Wax has her own practice and has been exclusively practicing immigration law since 2000.  She is on the Dedham Human Rights Commission and was adjunct clinical faculty for the Immigration Clinic at Boston College Law School for many years.  She is currently a committee chair in the Immigration Law Section of the Boston Bar Association.  Attorney Wax was the sole attorney at the Committee on Refugees from El Salvador for several years and also worked as a staff attorney at Catholic Charities.

Amy handles all types of immigration cases, including family-based petitions, consular processing, deportation, NACARA, asylum, naturalization and applications for relief for victims of domestic violence.  She is fluent in Spanish and Portuguese and frequently gives presentations to the Spanish and Portuguese-speaking communities.  She also has taught several years for Massachusetts Continuing Legal Education.  She holds a J.D. from Boston College Law School.

Amy has been a dedicated pro bono attorney for Project Citizenship providing a Crimmigration training, lending her immigration expertise, and serving on the Board.

The generous support of foundations, corporate and government sponsors has helped Project Citizenship to increase the naturalization rate in Boston and beyond. We are deeply grateful for their support.

Foundation Support
Amy Ensign-Barstow Memorial Fund at the East Bay Community Foundation

Aubert J. Fay Charitable Fund

Boston Bar Foundation

Brookline Community Foundation

Bushrod H. Campbell and Adah F. Hall Charity Fund

Cambridge Community Foundation

The Clowes Fund

Cummings Foundation

Eastern Bank Foundation

Ferrara Family Foundation

The Fish Family Foundation

Forest Foundation

The Granite Point Foundation

Greater Lowell Community Foundation

HarborOne Foundation

Klarman Family Foundation

Lincoln and Therese Filene Foundation

Massachusetts Bar Foundation

Mifflin Memorial Fund

Nathaniel and Elizabeth Stevens Foundation

One Percent for America

The Rabbi Abraham Halbfinger and Charlesview Charitable Fund at Charlesview, Inc.

The Rands Foundation

Theodore Edson Parker Foundation

Town Fair Tire Foundation

Tufts Community Grants

The Vertex Foundation

World of Change

Corporate Contributions
Affiliated Managers Group, Inc

Anthem Group

Bank of America

Bank of the West

Biogen

Brown Rudnick LLP

CCR Wealth Management

Fidelity Charitable Catalyst Fund

Foley Hoag

Goodwin Procter

Kirkland & Ellis LLP

Latham & Watkins LLP

Leader Bank

Liberty Mutual

MFS Investment Management

Morrison Foerster LLP

Morgan Lewis

PricewaterhouseCoopers

Red Hat

Ropes & Gray LLP

Seyfarth Shaw

Sun Life Financial

WilmerHale

Government Support
City of Boston / Mayor’s Office for Immigrant Advancement

Massachusetts Office for Refugees and Immigrants

U.S. Citizenship and Immigration Services (USCIS)

In-Kind Donations
CostCo

DC Rentals

Dunkin

FoodLink

Impact report: https://projectcitizenship.org/wp-content/uploads/2023/05/2022-Impact-Report-FINAL-2.pdf
To see previous years: https://projectcitizenship.org/annual-report/

"""

# Create a document
document = {
    "description": description
}

# Insert the document into the collection
result = collection.insert_one(document)

