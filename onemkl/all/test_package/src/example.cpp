#include <cassert>
#include <iostream>

#include <oneapi/mkl.hpp>
#include <sycl/sycl.hpp>

int main() {

  std::vector<float> a = {1.f, 2.f, 3.f, 4.f, 5.f};
  std::vector<float> b = {-1.f, 2.f, -3.f, 4.f, -5.f};

  sycl::context ctx;
  sycl::device dev{sycl::gpu_selector_v};
  sycl::queue q{ctx, dev};
  {
    sycl::buffer<float> buff_a(a.data(), a.size());
    sycl::buffer<float> buff_b(b.data(), b.size());

    // NOTE: if a segfault happens here it's because the ERROR_MSG is nullptr,
    // which means there are no enabled backend libraries.
    oneapi::mkl::blas::column_major::axpy(q, static_cast<long>(a.size()), 1.0f,
                                          buff_a, 1, buff_b, 1);
  }
  std::vector<float> expected = {0.f, 4.f, 0.f, 8.f, 0.f};

  std::cout << "{" << b[0] << ", " << b[1] << ", " << b[2] << ", " << b[3]
            << ", " << b[4] << "}\n";

  return static_cast<int>(b != expected);
}
