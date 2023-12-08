## Case Covid19 KaBum

### ETAPA 2 - Bigquery

#### 2 - Qual a quantidade de Casos confirmados por Estado, classificando os 5 primeiros estados com mais casos?

```
select 
    state,
    sum(confirmed) as total_confirmed
from 
    `covid.caso`
where 
    is_last = True
    and place_type = 'state'
group by 1
order by 2 desc   
```

#### 3 - Qual a Letalidade em % (mortes/casos confirmados) por Estado, classificando os 5 primeiros estados com maior letalidade ?

```
select
    state,
    deaths,
    confirmed,
    round(deaths / confirmed * 100, 3) as lethality
from 
    `covid.caso`
where
    is_last = True
    and place_type = 'state'
order by 4 desc
```
#### 4 - Qual a Taxa de Óbitos por cada mil habitantes, por estado , listar os 5 primeiros estados com maior concentração de óbitos por cada mil habitantes(população) ?

```
select
    state,
    deaths,
    estimated_population,
    round((deaths / estimated_population) * 1000, 2) as lethality
from 
    `covid.caso`
where
    is_last = True
    and place_type = 'state'
order by 4 desc
```

#### 5 - Qual a porcentagem de municípios que registraram óbito em relação ao total de municípios da amostra?
```
declare city_with_deaths int64;
declare all_city int64;

set city_with_deaths = (select count(*) from `covid.caso` where is_last = True and place_type in ('city') and deaths > 0 and estimated_population is not null);
set all_city = (select count(*) from `covid.caso` where is_last = True and place_type in ('city') and estimated_population is not null);

select all_city, city_with_deaths, round(city_with_deaths / all_city * 100, 2) as city_with_deaths_percent
```

#### 6 - Qual a população total por estado , o município mais populoso de cada estado e a representatividade de concentração populacional em porcentagem deste município em relação ao total de habitantes do estado ?

```
    create or replace temp table population_by_state as
    select
        state,
        sum(estimated_population) as estimated_population
    from
        `covid.caso`
    where
        is_last = True
        and place_type in ('state')
    group by 1
    order by 2 desc
    ;

    with most_popular_city as (
    select
        state,
        city,
        estimated_population,
        rank() over (partition by state order by estimated_population desc) as ranking
    from
        `covid.caso`
    where
        is_last = True
        and place_type in ('city')
    )

    select
        a.state,
        a.estimated_population,
        b.city as city,
        b.estimated_population as city_estimated_population,
        round((b.estimated_population / a.estimated_population) * 100, 2) as population_concentration
    from
        population_by_state a
        join most_popular_city b on a.state = b.state
    where
        ranking = 1
        order by 5 desc
```

### ETAPA 3 - Dashboard

#### Link Looker: <https://lookerstudio.google.com/s/kKMn5e88BWI>

#### ETAPA 3 (item 4)

##### Crie um gráfico de linhas que representam os casos confirmados acumulados dia a dia no Brasil.
