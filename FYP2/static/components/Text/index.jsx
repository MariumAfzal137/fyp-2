import React from "react";

const variantClasses = {
  h1: "font-normal sm:text-[40px] md:text-[46px] text-[50px]",
  h2: "font-semibold sm:text-[36px] md:text-[38px] text-[40px]",
  h3: "font-medium text-[18px]",
  h4: "font-medium text-[16px]",
  h5: "font-medium text-[13px]",
  h6: "font-normal text-[12px]",
};

const Text = ({ children, className, variant, as, ...restProps }) => {
  const Component = as || "span";
  return (
    <Component
      className={`${className} ${variant && variantClasses[variant]}`}
      {...restProps}
    >
      {children}
    </Component>
  );
};

export { Text };
