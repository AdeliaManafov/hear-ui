import {inject, provide} from 'vue'
import {featureDefinitionsStore} from './featureDefinitionsStore'

export const FeatureDefinitionsKey = Symbol('feature-definitions')

export const provideFeatureDefinitions = () => {
  provide(FeatureDefinitionsKey, featureDefinitionsStore)
}

export const useFeatureDefinitions = () => {
  const store = inject(FeatureDefinitionsKey, featureDefinitionsStore)
  return store
}
