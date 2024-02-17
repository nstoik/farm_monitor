import Request from '@/api/fetch'
import { type Grainbin, type GrainbinUpdate } from '@/interfaces/grainbin.interface'

export class GrainbinRequest extends Request {
  constructor() {
    super()
    this.resourceLocation = `${this.baseURL}grainbin/`
  }

  /**
   * A public function to get all grainbins from the database.
   *
   * @returns {Promise<Array<Grainbin>>} A promise that resolves to an array of grainbins.
   */
  public async getGrainbins(): Promise<Array<Grainbin>> {
    const url = `${this.resourceLocation}`
    return this.client.get(url).then((response) => {
      //convert any dates from string to Date objects
      // Add the timezone offset to the date to make it local time.
      response.data.forEach((grainbin: Grainbin) => {
        grainbin.lastUpdated = new Date(grainbin.lastUpdated + 'Z')
      })
      return response.data
    })
  }
  /**
   * A public function to get the latest set of updates for a given id from the database.
   *
   * @param id The ID of the grainbin to get the updates from.
   *
   * @returns {Promise<Array<GrainbinUpdate>>} An array of grainbin updates. This corresponds
   * to the latest set of grainbin updates. If there are no updates, an empty array is returned.
   */
  public async getGrainbinLatestUpdates(id: number): Promise<Array<GrainbinUpdate>> {
    const url = `${this.resourceLocation}${id}/updates/latest`
    return this.client.get(url).then((response) => {
      //convert any dates from string to Date objects
      // Add the timezone offset to the date to make it local time.
      response.data.forEach((grainbinUpdate: GrainbinUpdate) => {
        grainbinUpdate.timestamp = new Date(grainbinUpdate.timestamp + 'Z')
      })
      return response.data
    })
  }
}
