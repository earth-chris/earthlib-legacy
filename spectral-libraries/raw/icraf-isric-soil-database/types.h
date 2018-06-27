/******************************************************************/
/* THIS IS AN AUTOMATICALLY GENERATED FILE.  DO NOT EDIT IT!!!!!! */
/******************************************************************/
typedef struct _Chemical_properties
{
	char *	iso;
	int	id;
	int	hori;
	int	btop;
	int	bbot;
	char *	sampleno;
phh2o;
phkcl;
phcacl2;
caco3;
caso4;
orgc;
orgn;
	long	c/n;
ca;
mg;
na;
k;
sum;
exacid;
exal;
cecsoil;
	int	cecclay;
cecorg;
ecec;
	long	bs;
als;
	long	esp;
ec;
	char *	chemrem;
editdate;
	char *	verified;

} Chemical_properties ;

typedef struct _Classification
{
	char *	iso;
	int	id;
	char *	wrb_rg;
	char *	wrb_q1;
	char *	wrb_q2;
	char *	wrb_q3;
	char *	wrb_q4;
	char *	fao_88;
	char *	fsub_88;
	char *	pha_88;
faostat_88;
	char *	fao_74;
	char *	pha_74;
faostat;
	char *	usgg_99;
	char *	ussg_99;
	char *	ustx_92;
	char *	usmin_92;
	char *	str_92;
	char *	oth_92;
	char *	smr_92;
	char *	usgg_75;
	char *	ussg_75;
	char *	ustx;
	char *	usmin;
	char *	str;
	char *	oth;
	char *	smr;
	char *	local;
	char *	remarks;
editdate;
	char *	ver;

} Classification ;

typedef struct _Classification_key
{
	char *	attribute;
	char *	value;
	char *	description;
	int	order;

} Classification_key ;

typedef struct _Clay_mineralogy
{
	char *	iso;
	int	id;
	int	hori;
	int	top;
	int	bot;
	char *	sampleno;
	char *	kaol;
	char *	mill;
	char *	verm;
	char *	chlor;
	char *	smec;
	char *	hall;
	char *	mix;
	char *	quar;
	char *	feld;
	char *	gibb;
	char *	goet;
	char *	hem;
	char *	minx;
	char *	miny;
	char *	minz;
fe;
al;
ammfe;
ammal;
ammsi;
fep;
alp;
cp;
	int	pret;
phnaf;
odoe;
mi;
	char *	cminrem;
editdate;
	char *	verified;
	char *	codetype;
	char *	type;

} Clay_mineralogy ;

typedef struct _Climate_Data
{
	char *	iso;
	int	id;
	char *	type;
	int	nrecord;
annual;
jan;
feb;
mar;
apr;
may;
jun;
jul;
aug;
sep;
oct;
nov;
dec;
editdate;

} Climate_Data ;

typedef struct _Climate_Data_Big
{
	char *	iso;
	int	id;
	char *	type;
	int	nrecord;
annual;
jan;
feb;
mar;
apr;
may;
jun;
jul;
aug;
sep;
oct;
nov;
dec;
editdate;

} Climate_Data_Big ;

typedef struct _Climate_Station
{
	char *	iso;
	int	id;
wmocode;
	char *	statname;
	char *	lonew;
	int	lond;
	int	lonm;
	char *	latns;
	int	latd;
	int	latm;
	int	alt;
editdate;

} Climate_Station ;

typedef struct _Climate_Station_Big
{
	char *	iso;
	int	id;
wmocode;
	char *	station;
	char *	lonew;
	int	lond;
	int	lonm;
	char *	latns;
	int	latd;
	int	latm;
	int	alt;
editdate;

} Climate_Station_Big ;

typedef struct _Country
{
	char *	iso;
	char *	country;
	char *	region;

} Country ;

typedef struct _Elemental_composition_soil
{
	char *	iso;
	int	id;
	int	hori;
	int	top;
	int	bot;
	char *	sampleno;
sio2;
al2o3;
fe2o3;
cao;
mgo;
k2o;
na2o;
tio2;
mno2;
p2o5;
ign;
total;
ratiosial;
ratiosife;
ratiosir;
ratioalfe;
	char *	soelrem;
editdate;
	char *	verified;
	char *	codetype;

} Elemental_composition_soil ;

typedef struct _FAO74_diagnostic_horizons
{
	char *	iso;
	int	id;
	char *	dhor_74;
editdate;

} FAO74_diagnostic_horizons ;

typedef struct _FAO74_diagnostic_properties
{
	char *	iso;
	int	id;
	char *	dpro_74;
editdate;

} FAO74_diagnostic_properties ;

typedef struct _FAO88_diagnostic_horizons
{
	char *	iso;
	int	id;
	char *	fhor_88;
editdate;

} FAO88_diagnostic_horizons ;

typedef struct _FAO88_diagnostic_properties
{
	char *	iso;
	int	id;
	char *	fpro_88;
editdate;

} FAO88_diagnostic_properties ;

typedef struct _ASD Spectra
{
	char *	batch_labid;
w350;
w360;
w370;
w380;
w390;
w400;
w410;
w420;
w430;
w440;
w450;
w460;
w470;
w480;
w490;
w500;
w510;
w520;
w530;
w540;
w550;
w560;
w570;
w580;
w590;
w600;
w610;
w620;
w630;
w640;
w650;
w660;
w670;
w680;
w690;
w700;
w710;
w720;
w730;
w740;
w750;
w760;
w770;
w780;
w790;
w800;
w810;
w820;
w830;
w840;
w850;
w860;
w870;
w880;
w890;
w900;
w910;
w920;
w930;
w940;
w950;
w960;
w970;
w980;
w990;
w1000;
w1010;
w1020;
w1030;
w1040;
w1050;
w1060;
w1070;
w1080;
w1090;
w1100;
w1110;
w1120;
w1130;
w1140;
w1150;
w1160;
w1170;
w1180;
w1190;
w1200;
w1210;
w1220;
w1230;
w1240;
w1250;
w1260;
w1270;
w1280;
w1290;
w1300;
w1310;
w1320;
w1330;
w1340;
w1350;
w1360;
w1370;
w1380;
w1390;
w1400;
w1410;
w1420;
w1430;
w1440;
w1450;
w1460;
w1470;
w1480;
w1490;
w1500;
w1510;
w1520;
w1530;
w1540;
w1550;
w1560;
w1570;
w1580;
w1590;
w1600;
w1610;
w1620;
w1630;
w1640;
w1650;
w1660;
w1670;
w1680;
w1690;
w1700;
w1710;
w1720;
w1730;
w1740;
w1750;
w1760;
w1770;
w1780;
w1790;
w1800;
w1810;
w1820;
w1830;
w1840;
w1850;
w1860;
w1870;
w1880;
w1890;
w1900;
w1910;
w1920;
w1930;
w1940;
w1950;
w1960;
w1970;
w1980;
w1990;
w2000;
w2010;
w2020;
w2030;
w2040;
w2050;
w2060;
w2070;
w2080;
w2090;
w2100;
w2110;
w2120;
w2130;
w2140;
w2150;
w2160;
w2170;
w2180;
w2190;
w2200;
w2210;
w2220;
w2230;
w2240;
w2250;
w2260;
w2270;
w2280;
w2290;
w2300;
w2310;
w2320;
w2330;
w2340;
w2350;
w2360;
w2370;
w2380;
w2390;
w2400;
w2410;
w2420;
w2430;
w2440;
w2450;
w2460;
w2470;
w2480;
w2490;
w2500;

} ASD Spectra ;

typedef struct _Key
{
	char *	attribute;
	char *	value;
	char *	description;
fao77;
fao90;
	char *	key_id;
order;

} Key ;

typedef struct _Morphology_I
{
	char *	iso;
	int	id;
	int	hori;
	char *	symbol;
	int	top;
	int	bot;
	char *	wid;
	char *	tpg;
	char *	hued;
vald;
chromd;
	char *	hue;
value;
chroma;
	char *	grade;
	char *	size;
	char *	form;
	char *	fore;
	char *	grade2;
	char *	size2;
	char *	form2;
	char *	fieldtx;
	char *	txmod;
	char *	orgk;
	char *	orgd;
	char *	cond;
	char *	conm;
	char *	conws;
	char *	conwp;
	char *	cono;
	char *	porq;
	char *	porq1;
	char *	porq2;
	char *	porq21;
	char *	pors;
	char *	pors1;
	char *	pors2;
	char *	pors21;
	char *	porc;
	char *	porc2;
	char *	pord;
	char *	pord2;
	char *	porf;
	char *	porf2;
	char *	poro;
	char *	poro2;
	char *	port;
	char *	roq;
	char *	roq2;
	char *	ros;
	char *	ros2;
	char *	rol;
	char *	rol2;
	char *	effa;
	char *	effc;
	char *	effl;
phval;
	char *	remarks;
editdate;
	char *	ver;

} Morphology_I ;

typedef struct _Morphology_II
{
	char *	iso;
	int	id;
	int	hori;
	char *	motta;
	char *	motta2;
	char *	motts;
	char *	motts2;
	char *	mottc;
	char *	mottc2;
	char *	mottb;
	char *	mottb2;
	char *	motthue;
mottval;
mottch;
	char *	motthu2;
mottva2;
mottch2;
	char *	cutc;
	char *	cutt;
	char *	cutk;
	char *	cutl;
	char *	incq;
	char *	incq2;
	char *	inct;
	char *	inct2;
	char *	incsi;
	char *	incsi2;
	char *	inch;
	char *	inch2;
	char *	incsh;
	char *	incsh2;
	char *	incc;
	char *	incc2;
	char *	rockq;
	char *	rockq2;
	char *	rocks;
	char *	rocks2;
	char *	rockw;
	char *	rockw2;
	char *	rockc;
	char *	rockc2;
	char *	pank;
	char *	panc;
	char *	pany;
	char *	pans;
	char *	bioa;
	char *	biok;
	char *	biok2;
editdate;
	char *	ver;

} Morphology_II ;

typedef struct _Physical_properties
{
	char *	iso;
	int	id;
	int	hori;
	int	btop;
	int	bbot;
	char *	sampleno;
gravel;
s1;
s2;
s3;
s4;
s5;
tsa;
si1;
si2;
tsi;
clay;
dispcl;
bulk;
pf0;
pf1;
pf15;
pf2;
pf23;
pf27;
pf34;
pf42;
cole;
ssa;
	char *	physrem;
editdate;
	char *	verified;
	char *	codetype;
	char *	type;

} Physical_properties ;

typedef struct _Region
{
	char *	region;
	char *	name;

} Region ;

typedef struct _Sand_mineralogy_general
{
	char *	iso;
	int	id;
	int	hori;
	int	top;
	int	bot;
	char *	sampleno;
heavy;
light;
	int	quartz;
	int	k_feldspar;
	int	plagioclas;
	int	rest;
	int	opaque;
	char *	sminrem;
editdate;
	char *	verified;

} Sand_mineralogy_general ;

typedef struct _Sand_mineralogy_minerals
{
	char *	sampleno;
	char *	mineral;
	int	value;

} Sand_mineralogy_minerals ;

typedef struct _Site_description
{
	char *	iso;
	int	id;
smonth;
	int	syear;
	char *	auth;
	char *	loc;
	char *	latns;
	int	latd;
	int	latm;
	int	lats;
	char *	lonew;
	int	lond;
	int	lonm;
	int	lons;
	int	alt;
	char *	clim;
	char *	par;
	char *	par2;
	char *	mode;
	char *	mode2;
	char *	text;
	char *	text2;
	int	depth;
	char *	weat;
	char *	weat2;
	char *	rest1;
	char *	rest2;
	char *	parrem;
	char *	lndreg;
	char *	lndtop;
	char *	phys;
slp;
	char *	pos;
	char *	slf;
	char *	asp;
	char *	knd;
	char *	ptrn;
	int	var;
	char *	rock;
	char *	ston;
stsi;
	char *	stsh;
	char *	cra;
	char *	sea;
	char *	salt;
	char *	alkali;
	int	sode;
	char *	wake;
	int	wade;
	int	waup;
	int	walo;
	int	staup;
	int	stalo;
	char *	stape;
	char *	run;
	char *	flfr;
	char *	flna;
	char *	drain;
	char *	draini;
	int	moidu;
	int	moidl;
	int	moimu;
	int	moiml;
	int	moiwu;
	int	moiwl;
	char *	ert;
	char *	ert2;
	char *	erd;
	char *	erd2;
	char *	aggr;
	char *	mass;
	char *	lut;
	char *	crop;
	char *	irr;
	char *	rot;
	char *	imp;
	char *	vet;
	char *	ves;
	char *	ved;
adpc;
admm;
	char *	comname;
	char *	descr;
	char *	remarks;
editdate;
	char *	verified;

} Site_description ;

typedef struct _Soil_colour
{
	char *	hue;
value;
chroma;
	char *	colourcode;
	char *	name;

} Soil_colour ;

typedef struct _Soluble_salts
{
	char *	iso;
	int	id;
	int	hori;
	int	top;
	int	bot;
	char *	sampleno;
cas;
mgs;
nas;
ks;
sumcat;
co3;
hco3;
cl;
so4;
no3;
sumani;
ec5;
ece;
phs;
sar;
	char *	saltrem;
editdate;
	char *	verified;
	char *	type;

} Soluble_salts ;

typedef struct _ST_diagnostic_horizons
{
	char *	iso;
	int	id;
	char *	uhor_92;
editdate;

} ST_diagnostic_horizons ;

typedef struct _ST_diagnostic_properties
{
	char *	iso;
	int	id;
	char *	upro_92;
editdate;

} ST_diagnostic_properties ;

typedef struct _Trace_elements
{
	char *	iso;
	long	id;
	long	top;
	long	bott;
	char *	sampleno;
as;
	long	ba;
cd;
	long	co;
	long	cr;
	long	cu;
	long	mn;
mo;
	long	ni;
	long	pb;
	long	sr;
	long	v;
	long	zn;
	char *	te_rem;
date;
	char *	ver;

} Trace_elements ;

typedef struct _WRB_diagnostic_materials
{
	char *	iso;
	int	id;
	char *	wrb_m;
editdate;

} WRB_diagnostic_materials ;

typedef struct _WRB_diagnostic_properties
{
	char *	iso;
	int	id;
	char *	wrb_p;
editdate;

} WRB_diagnostic_properties ;

typedef struct _Elemental_composition_clay
{
	char *	iso;
	int	id;
	int	hori;
	int	top;
	int	bot;
	char *	sampleno;
sio2;
al2o3;
fe2o3;
cao;
mgo;
k2o;
na2o;
tio2;
mno2;
p2o5;
ign;
total;
ratiosial;
ratiosife;
ratiosir;
ratioalfe;
	char *	soelrem;
editdate;
	char *	verified;

} Elemental_composition_clay ;

typedef struct _Profile-climate_station_link
{
	char *	iso_p;
	int	id_p;
	char *	iso_s;
	int	id_s;
	int	dist;
	char *	dir;
	char *	ref;
editdate;

} Profile-climate_station_link ;

typedef struct _WRB_diagnostic_horizons
{
	char *	iso;
	int	id;
	char *	wrb_h;
editdate;

} WRB_diagnostic_horizons ;

typedef struct _ICRAF sample codes
{
	char *	batch and labid;
	char *	sampleno;
	char *	country name;
	char *	plotcode;
hori;
btop;
bbot;
dsed;

} ICRAF sample codes ;

