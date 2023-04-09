/* Prerequisite Item. */

export enum ItemType {
  repository = "Repo",
  file = "File",
}
/**
 * Contain some metadata of item.
 * 
 * @param name Named by author.
 * @param uniqueId
 * @param type
*/
export interface ItemMeta {
  name: string;
  uniqueId: string | number;
  type: ItemType;
};
export type ItemTitle = string;
/**
 * May a complex type.
*/
export type ItemDescription = any;

/**
 * Provide items in application.
 */
export interface Item {
  metadata: ItemMeta;
  link: string; // URL.
}


export function addItem() { }


export function updateItem() { }


export function contains() { }
