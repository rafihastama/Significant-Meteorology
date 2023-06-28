import CONFIG from '../globals/config'

const CacheHelper = {
  async cachingAppShell (requests) {
    const cache = await this._openCache()
    cache.addAll(requests)
  },

  async deleteOldCache () {
    const cacheNames = await caches.keys()
    cacheNames
      .filter((name) => name !== CONFIG.CACHE_NAME)
      .map((filteredName) => caches.delete(filteredName))
  },

  async revalidateCache (request) {
    const cacheResponse = await caches.match(request)

    if (cacheResponse) {
      return cacheResponse
    }

    return this._fetchRequest(request)
  },

  async _openCache () {
    return caches.open(CONFIG.CACHE_NAME)
  },

  async _fetchRequest (request) {
    try {
      const response = await fetch(request)

      return response
    } catch (error) {
      console.error('Error fetching resource:', error)
      return null
    }
  },

  async _cachePage (request, response) {
    const cache = await this._openCache()
    cache.put(request, response)
  }
}

export default CacheHelper
