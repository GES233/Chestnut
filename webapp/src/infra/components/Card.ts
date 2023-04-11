import { Image } from "./Image";


/**
 * The type of Card Component in TinyUI.
 * 
 * @param title Title of Card
 * @param image `Image` instance
 * @param content
 * @param categories List of categories
*/
export type CardModel = {
  title: string,
  image: Image,
  content: string,
  categories: any,
};
