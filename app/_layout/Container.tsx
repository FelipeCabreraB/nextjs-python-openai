type Props = {
  children: React.ReactNode;
  className?: string;
};

const Container = ({ children, className }: Props) => {
  return (
    <section className="max-w-5xl mx-auto">
      <div className={className}>{children}</div>
    </section>
  );
};

export default Container;
