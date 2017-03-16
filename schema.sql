/*drop table if exists term_deposit;*/

create table term_deposit (
    id integer primary key autoincrement,
    name text not null,
    logo text,
    product text not null,
    notes text,
    one_month text not null,
    two_month text not null,
    three_month text not null,
    four_month text not null,
    five_month text not null,
    six_month text not null,
    seven_month text not null,
    eight_month text not null,
    nine_month text not null,
    ten_month text not null,
    eleven_month text not null,
    twelve_month text not null,
    twentyfour_month text not null,
    thirtysix_month text not null,
    date real
);

/*drop table if exists online_saver;*/

create table online_saver (
    id integer primary key autoincrement,
    name text not null,
    logo text,
    product text not null,
    notes text,
    base text not null,
    bonus text not null,
    total text not null,
    date real
);

/*drop table if exists progress_saver;*/

create table progress_saver (
    id integer primary key autoincrement,
    name text not null,
    logo text,
    product text not null,
    notes text,
    base text not null,
    bonus text not null,
    total text not null,
    date real
);


/*drop table if exists cash_manager;*/

create table cash_manager (
    id integer primary key autoincrement,
    name text not null,
    logo text,
    product text not null,
    notes text,
    _500k text not null,
    _250k text not null,
    _100k text not null,
    _50k text not null,
    date real
);

/*drop table if exists pensioner;*/

create table pensioner (
    id integer primary key autoincrement,
    name text not null,
    logo text,
    product text not null,
    notes text,
    _5k text not null,
    _2k text not null,
    _0k text not null,
    date real
);

