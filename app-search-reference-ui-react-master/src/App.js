import React from "react";
import './styles.css';

import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";

import {
  ErrorBoundary,
  Facet,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  Sorting,
  WithSearch
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

import {
  buildAutocompleteQueryConfig,
  buildFacetConfigFromConfig,
  buildSearchOptionsFromConfig,
  buildSortOptionsFromConfig,
  getConfig,
  getFacetFields,
  getResultTitle
} from "./config/config-helper";

const { hostIdentifier, searchKey, endpointBase, engineName } = getConfig();
const connector = new ElasticsearchAPIConnector({host: "http://localhost:9200", index: "partidos"});
const config = {
  searchQuery: {
    facets: buildFacetConfigFromConfig(),
    ...buildSearchOptionsFromConfig()
  },
  autocompleteQuery: buildAutocompleteQueryConfig(),
  apiConnector: connector,
  alwaysSearchOnInitialLoad: true
};

// Componente personalizado para renderizar resultados
const CustomResultView = ({ result }) => {
  const homeTeam = result.home_team?.raw || "Equipo local";
  const awayTeam = result.away_team?.raw || "Equipo visitante";

  const homeScorers = [
    {
      name: result.home_team_goalscorer1_name?.raw,
      goals: result.home_team_goalscorer1_goals?.raw,
      games: result.home_team_goalscorer1_games_played?.raw,
      ratio: result.home_team_goalscorer1_goal_ratio?.raw,
    },
    {
      name: result.home_team_goalscorer2_name?.raw,
      goals: result.home_team_goalscorer2_goals?.raw,
      games: result.home_team_goalscorer2_games_played?.raw,
      ratio: result.home_team_goalscorer2_goal_ratio?.raw,
    },
    {
      name: result.home_team_goalscorer3_name?.raw,
      goals: result.home_team_goalscorer3_goals?.raw,
      games: result.home_team_goalscorer3_games_played?.raw,
      ratio: result.home_team_goalscorer3_goal_ratio?.raw,
    },
  ];

  const awayScorers = [
    {
      name: result.away_team_goalscorer1_name?.raw,
      goals: result.away_team_goalscorer1_goals?.raw,
      games: result.away_team_goalscorer1_games_played?.raw,
      ratio: result.away_team_goalscorer1_goal_ratio?.raw,
    },
    {
      name: result.away_team_goalscorer2_name?.raw,
      goals: result.away_team_goalscorer2_goals?.raw,
      games: result.away_team_goalscorer2_games_played?.raw,
      ratio: result.away_team_goalscorer2_goal_ratio?.raw,
    },
    {
      name: result.away_team_goalscorer3_name?.raw,
      goals: result.away_team_goalscorer3_goals?.raw,
      games: result.away_team_goalscorer3_games_played?.raw,
      ratio: result.away_team_goalscorer3_goal_ratio?.raw,
    },
  ];

  const renderScorers = (scorers) =>
    scorers
      .filter((scorer) => scorer.name) // Filtrar los goleadores no definidos
      .map((scorer, index) => (
        <li key={index}>
          <strong>{scorer.name}</strong>: {scorer.goals} goles en {scorer.games} partidos ({scorer.ratio} goles/partido)
        </li>
      ));

  return (
    <div className="custom-result">
      <h2>{`${homeTeam} - ${awayTeam}`}</h2>
      {/* Puedes incluir más detalles aquí, si es necesario */}
      <p>Temporada: {result.season?.raw}</p>
      <p>Categoría: {result.category?.raw}</p>
      <p>Grupo: {result.group?.raw}</p>
      <p>Jornada: {result.match_week?.raw}</p>
      <p>Árbitro: {result.referee?.raw}</p>
      <p>Fecha: {result.date?.raw}</p>
      <p>Hora: {result.time?.raw}</p>
      <p>Campo: {result.field?.raw}</p>
      <p>Superficie: {result.field_type?.raw}</p>
      <p>Localidad: {result.field_city?.raw}</p>
      <p>Dirección: {result.field_direction?.raw}</p>

      <div className="scorers-section">
        <h3>Máximos goleadores:</h3>
        <div className="team-scorers">
          <h4>{homeTeam}</h4>
          <ul>{renderScorers(homeScorers)}</ul>
        </div>
        <div className="team-scorers">
          <h4>{awayTeam}</h4>
          <ul>{renderScorers(awayScorers)}</ul>
        </div>
      </div>
    </div>
  );
};

export default function App() {
  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                <Layout
                  header={<SearchBox autocompleteSuggestions={true} />}
                  sideContent={
                    <div>
                      {wasSearched && (
                        <Sorting
                          label={"Sort by"}
                          sortOptions={buildSortOptionsFromConfig()}
                        />
                      )}
                      {getFacetFields().map(field => {
                        if(field == "match_week") {
                          return <Facet key={field} field={field} label={"Jornada"} />
                        } else if(field == "field_city") {
                          return <Facet key={field} field={field} label={"Localidad"} />
                        }
                      })}
                    </div>
                  }
                  bodyContent={
                    <Results
                      titleField={CustomResultView}
                      urlField={getConfig().urlField}
                      thumbnailField={getConfig().thumbnailField}
                      resultView={CustomResultView}
                      shouldTrackClickThrough={true}
                    />
                  }
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo />}
                      {wasSearched && <ResultsPerPage />}
                    </React.Fragment>
                  }
                  bodyFooter={<Paging />}
                />
              </ErrorBoundary>
            </div>
          );
        }}
      </WithSearch>
    </SearchProvider>
  );
}
