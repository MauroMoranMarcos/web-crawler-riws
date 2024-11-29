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

  return (
    <div className="custom-result">
      <h2>{`${homeTeam} - ${awayTeam}`}</h2>
      {/* Puedes incluir más detalles aquí, si es necesario */}
      <p>Temporada: {result.season?.raw}</p>
      <p>Categoría: {result.category?.raw}</p>
      <p>Grupo: {result.group?.raw}</p>
      <p>Jornada: {result.match_week?.raw}</p>
      <p>Fecha: {result.date?.raw}</p>
      <p>Hora: {result.time?.raw}</p>
      <p>Campo: {result.field?.raw}</p>
      <p>Árbitro: {result.referee?.raw}</p>
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
                      {getFacetFields().map(field => (
                        <Facet key={field} field={field} label={field} />
                      ))}
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
