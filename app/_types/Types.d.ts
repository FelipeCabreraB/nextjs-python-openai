type Products = {
  products: Product[];
};

interface ProductCard {
  product: Product;
}

type Product = {
  id: string;
  name: string;
  price?: number;
  description?: string;
  image?: string;
  images?: { file: { url: string } }[];
  slug?: string;
  currency?: string;
};
