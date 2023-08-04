"use client";

import Image from "next/image";
import Link from "next/link";

interface Props {
  product: {
    name: string;
    images: {
      file: {
        url: string;
      };
    }[];
    slug: string;
    price: number;
    currency?: string;
    image?: string;
  };
}

const ProductCard = ({ product }: Props) => {
  return (
    <div
      data-cy="product-card"
      className="flex flex-col justify-between border-l lg:border-l-0 border-r max-w-md border-gray transition-all duration-300 w-full bg-white hover:scale-105"
    >
      <div className="px-5 py-4">
        <div className="flex mx-auto cursor-pointer relative max-w-full max-h-full h-[436px]">
          <Link href={`/product/${product.slug}`} data-cy="product-link">
            <Image
              src={
                (product.images
                  ? product.images[0].file.url
                  : product.image) || '/img/not-found.png' as string
              }
              alt={product.name}
              fill
              style={{ objectFit: "cover" }}
            />
          </Link>
        </div>
        <p
          data-cy="product-name"
          className="font-quicksand mt-3 mb-3 uppercase line-clamp-2 h-12"
        >
          {product.name}
        </p>
        <div className="mt-auto">
          <p className="font-quicksand font-bold">
            $<span className="ml-2">{product.price}</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
