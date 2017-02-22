drop table if exists term_deposit;
create table term_deposit (
    id integer primary key autoincrement,
    name text not null,
    logo text not null,
    short text,
    short_rate text,
    mid text,
    mid_rate text,
    long text,
    long_rate text,
    date real
)
