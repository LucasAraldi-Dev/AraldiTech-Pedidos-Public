module.exports = {
  preset: '@vue/cli-plugin-unit-jest',
  // Diretórios onde os testes serão procurados
  testMatch: [
    "**/tests/unit/**/*.spec.[jt]s?(x)",
    "**/__tests__/*.[jt]s?(x)"
  ],
  // Diretórios a serem excluídos da coleta de cobertura
  coveragePathIgnorePatterns: [
    "/node_modules/",
    "/tests/",
    "/__tests__/"
  ],
  // Limites mínimos de cobertura
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  // Transformações para os arquivos
  transform: {
    '^.+\\.vue$': 'vue-jest',
    '^.+\\.js$': 'babel-jest'
  },
  // Módulos a serem transformados
  transformIgnorePatterns: [
    '/node_modules/(?!(@vue|vue-router|vuex)/)'
  ],
  // Configuração para Vue Test Utils
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': '<rootDir>/tests/unit/mocks/styleMock.js',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/tests/unit/mocks/fileMock.js'
  },
  // Configuração de ambiente
  testEnvironment: 'jsdom',
  // Configuração para arquivos de instalação e desmontagem de testes
  setupFilesAfterEnv: [
    '<rootDir>/tests/unit/setup.js'
  ],
  // Ignorar arquivos específicos
  testPathIgnorePatterns: [
    '/node_modules/',
    '/dist/'
  ],
  // Exibir saída detalhada de testes
  verbose: true,
  // Gerar relatório de cobertura
  collectCoverage: true,
  collectCoverageFrom: [
    'src/**/*.{js,vue}',
    '!src/main.js',
    '!src/router.js',
    '!**/node_modules/**'
  ],
  // Formatos de relatório de cobertura
  coverageReporters: [
    "json",
    "lcov",
    "text",
    "clover"
  ]
}; 